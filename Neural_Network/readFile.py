import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import PowerNorm

TRACK_PATHS=["images/Track1.png","images/Track2.png","images/Track3.png"]
#C:\Users\franj\Desktop\Universidade\3_ano\2_semestre\Trabalhos_Praticos\FIA\_Pt2\images\Track3.png
os.makedirs("output", exist_ok=True)

geracoes = []
fitness = []
def main(track_number):
    txt_path = "results" + str(track_number+1)

    track = plt.imread(TRACK_PATHS[track_number])
    #--------------------------------#
    #          Fitness Plot          #
    #--------------------------------#
    with open("./Neural_Network/"+txt_path+"/fitness.txt", "r") as file:
        linhas = file.readlines()

    for linha in linhas[1:]:
        partes = linha.split()
        geracoes.append(int(partes[0]))
        fitness.append(float(partes[1]))
    # Fitness plot per generation
    plt.figure()
    plt.plot(geracoes, fitness)
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Fitness evolution")

    death_pos = []
    #----------------------------------------------#
    #          Death Points on track Plot          #
    #----------------------------------------------#
    with open("./Neural_Network/"+txt_path+"/deaths.txt", "r") as file:
        linhas = file.readlines()
    for linha in linhas[1:]:
        partes = linha.split()
        death_pos.append((float(partes[1]), float(partes[2])))
    # Converting to np arrays
    death_pos = np.array(death_pos)
    # Plot of death points on the track
    plt.figure()
    plt.imshow(track)
    plt.scatter(death_pos[:, 0], death_pos[:, 1], c='r')
    plt.axis('off')
    plt.title("Crash Positions on track")
    plt.savefig("./Neural_Network/"+txt_path+"/crash_positions.jpeg", dpi=300, bbox_inches='tight')


    try:
        inf = {}
        max_t = 0
        with open(f"./Neural_Network/{txt_path}/best_behaviour.txt", "r") as file2:
            linhas = file2.readlines()

        for linha in linhas[1:]:
            partes = linha.split()
            geracao = int(partes[0])
            t = float(partes[1])
            if t > max_t:
                max_t = t
            dados = np.array([[float(partes[1]), float(partes[2]), float(partes[3]),
                            float(partes[4]), float(partes[5]), float(partes[6])]])    
            if geracao not in inf:
                inf[geracao] = dados
            else:
                inf[geracao] = np.vstack([inf[geracao], dados])

        output_folder = f"./Neural_Network/{txt_path}/frames"
        os.makedirs(output_folder, exist_ok=True)
        accel_paths = []
        speed_paths = []

        cmap = plt.get_cmap("jet")

        for key in inf:
            dados = inf[key]

            x = dados[:, 4]
            y = dados[:, 5]
            acel = dados[:, 2]
            speed = dados[:, 3]

            for i in range(1, len(x)):
                # Points up to i
                points = np.array([x[:i+1], y[:i+1]]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)

                # ACCELERATION FRAME
                fig = plt.figure()
                plt.imshow(track)
                lc = LineCollection(segments, cmap=cmap)
                lc.set_array(acel[:i])
                lc.set_clim(-1, 1)
                lc.set_linewidth(2)
                plt.gca().add_collection(lc)
                plt.axis('off')
                plt.title(f"Acceleration - Best Gen: {key}")
                plt.colorbar(lc, label="Acceleration")
                acc_path = f"{output_folder}/accel_{i:04d}.png"
                plt.savefig(acc_path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                accel_paths.append(acc_path)

                # SPEED FRAME
                fig = plt.figure()
                plt.imshow(track)
                lc = LineCollection(segments, cmap=cmap)
                lc.set_array(speed[:i])
                lc.set_clim(0, 100)  # ajusta o máximo de velocidade esperado
                lc.set_linewidth(2)
                plt.gca().add_collection(lc)
                plt.axis('off')
                plt.title(f"Speed - Best Gen: {key}")
                plt.colorbar(lc, label="Speed")
                speed_path = f"{output_folder}/speed_{i:04d}.png"
                plt.savefig(speed_path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                speed_paths.append(speed_path)

        # Criação dos GIFs
        acc_gif_path = f"./Neural_Network/{txt_path}/trajectory_acceleration.gif"
        speed_gif_path = f"./Neural_Network/{txt_path}/trajectory_speed.gif"

        if accel_paths:
            images = [imageio.imread(f) for f in accel_paths]
            imageio.mimsave(acc_gif_path, images, fps=20)

        if speed_paths:
            images = [imageio.imread(f) for f in speed_paths]
            imageio.mimsave(speed_gif_path, images, fps=20)

        # Opcional: limpar os frames
        for f in accel_paths + speed_paths:
            os.remove(f)

        print(f"GIFs criados: {acc_gif_path} e {speed_gif_path}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar os GIFs: {e}")


    #-------------------------------------------------------------#
    #      Plot of  acceleration, braking, speed and braking      # 
    #             in the track for saved generations              #
    #-------------------------------------------------------------#

    try:
        saved = {}
        inf = {}
        max_t = 0
        with open("./Neural_Network/"+txt_path+"/save_behaviour.txt", "r") as file:
            linhas = file.readlines()

        for linha in linhas[1:]:
            partes = linha.split()
            geracao = int(partes[0])
            t = float(partes[1])
            if t > max_t:
                max_t = t
            dados = np.array([[float(partes[1]), float(partes[2]), float(partes[3]),
                            float(partes[4]), float(partes[5]), float(partes[6])]])    
            if geracao not in inf:
                inf[geracao] = dados
            else:
                inf[geracao] = np.vstack([inf[geracao], dados])
        
        os.makedirs("output/frames_acc", exist_ok=True)
        os.makedirs("output/frames_speed", exist_ok=True)

        frame_paths_acc = []
        frame_paths_speed = []
        cmap = plt.get_cmap("jet")

        for gen in saved:
            # --- ACCELERATION FRAME ---
            fig_acc = plt.figure()
            plt.imshow(track)
            x = saved[gen][:, 4]
            y = saved[gen][:, 5]
            acel = saved[gen][:, 2]
            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, cmap=cmap)
            lc.set_array(acel)
            lc.set_clim(-1, 1)
            lc.set_linewidth(2)
            plt.gca().add_collection(lc)
            plt.axis('off')
            plt.title(f"Trajectory - Gen {gen}")
            plt.colorbar(lc, label="Acceleration")
            frame_filename_acc = f"output/frames_acc/frame_{gen:03d}.png"
            plt.savefig(frame_filename_acc)
            frame_paths_acc.append(frame_filename_acc)
            plt.close(fig_acc)
            print(f"size array: {frame_paths_acc.shape}")

            # --- SPEED FRAME ---
            fig_speed = plt.figure()
            plt.imshow(track)
            speed = saved[gen][:, 3]
            lc = LineCollection(segments, cmap=cmap)
            lc.set_array(speed)
            lc.set_clim(0, 100)  # Assuming speed range
            lc.set_linewidth(2)
            plt.gca().add_collection(lc)
            plt.axis('off')
            plt.title(f"Trajectory - Gen {gen}")
            plt.colorbar(lc, label="Speed")
            frame_filename_speed = f"output/frames_speed/frame_{gen:03d}.png"
            plt.savefig(frame_filename_speed)
            frame_paths_speed.append(frame_filename_speed)
            plt.close(fig_speed)
            print(f"size array: {frame_paths_speed.shape}")

        # Create GIFs
        gif_path_acc = f"output/trajectory_acceleration_track{track_number+1}.gif"
        gif_path_speed = f"output/trajectory_speed_track{track_number+1}.gif"
        print(f'size={len(frame_paths_acc)}')
        print(f'size={len(frame_paths_speed)}')
        imageio.mimsave(gif_path_acc, [imageio.imread(f) for f in frame_paths_acc], fps=2)
        imageio.mimsave(gif_path_speed, [imageio.imread(f) for f in frame_paths_speed], fps=2)

        # Delete frame images
        for f in frame_paths_acc:
            os.remove(f)
        for f in frame_paths_speed:
            os.remove(f)

        print(f"GIFs saved at {gif_path_acc} and {gif_path_speed}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar os GIFs: {e}")


    #-----------------------------------------------------------------------------#
    #      Plot of acceleration, braking, steering and speed during sim time      #
    #-----------------------------------------------------------------------------#
    fig1, (ax1) = plt.subplots(1,1, figsize=(10, 5))
    fig2, (ax2) = plt.subplots(1,1, figsize=(10, 5))
    fig3, (ax3) = plt.subplots(1,1, figsize=(10, 5))
    for gen in inf:
        ax1.plot(inf[gen][:,0], inf[gen][:,2], label=f'{gen}')
        ax2.plot(inf[gen][:,0], inf[gen][:,1], label=f'{gen}')
        ax3.plot(inf[gen][:,0], inf[gen][:,3], label=f'{gen}')

    ax1.set_title('Acceleration during simulation time',size=10)
    ax1.set_xlabel('Time (s)',size=10)
    ax1.set_ylabel('Acceleration',size=10)
    ax1.set_xlim(0, max_t)
    ax1.set_ylim(-1.1,1.1)

    ax2.set_title('Steering during simulation time',size=10)
    ax2.set_xlabel('Time (s)',size=10)
    ax2.set_ylabel('Steering',size=10)
    ax2.set_xlim(0, max_t)
    ax2.set_ylim(-1.1,1.1)

    ax3.set_title('Speed during simulation time',size=10)
    ax3.set_xlabel('Time (s)',size=10)
    ax3.set_ylabel('Velocidade',size=10)
    ax3.set_xlim(0, max_t)
    ax3.set_ylim(0,101)

    fig1.subplots_adjust(hspace=0.3)
    fig2.subplots_adjust(hspace=0.3)

    fig1.savefig("./Neural_Network/"+txt_path+"/acc.jpeg", dpi=300, bbox_inches='tight')
    fig2.savefig("./Neural_Network/"+txt_path+"/steering.jpeg", dpi=300, bbox_inches='tight')
    fig3.savefig("./Neural_Network/"+txt_path+"/speed.jpeg", dpi=300, bbox_inches='tight')

