import math
import os
import imageio
import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.image as mpimg
from multiprocessing import Process

TRACK_PATHS=["images/Track1.png","images/Track2.png","images/Track3.png","images/Track4.png","images/Track5.png"]

# opcao 0 faz todos os graficos
# opcao 1 faz tudo, graficos e gifs
# opcao 2 faz a evolucao de fitness
# opcao 3 faz o grafico de acidentes
# opcao 4 faz os graficos de velocidade, aceleracao e steering ao longo do tempo
# opcao 5 faz os graficos de velocidade e aceleracao na pista
# opcao 6 faz os gifs que mostram a velocidade e aceleracao ao longo do tempo na pista
# opcao 7, saved_option faz as opcoes 4, 5 e 6 se escolhidas para possíveis geracoes guardadas

def main(track_number, options, gifs=False, saved_option=False):
    track_path=TRACK_PATHS[track_number]
    track = mpimg.imread(track_path)
    results_path = 'results' + str(track_number+1)

    best_data = saved_data = None
    if any(opt in [0, 1, 4, 5] for opt in options) or gifs:
        best_data, max_t = get_behaviour_data(results_path)
    if saved_option and any(opt in [0, 1, 4, 5] for opt in options) or gifs:
        saved_data, max_t_s = get_behaviour_data(results_path, filename='save_behaviour.txt')

    
    if 0 in options or 1 in options or 2 in options:
        graph_fitness(results_path)

    # Acidentes
    if 0 in options or 1 in options or 3 in options:
        graph_crash(results_path, track)

    # Dados normais
    if best_data:
        if any(opt in [0, 1, 4, 5] for opt in options):
            graphs_acc_speed_time(results_path, best_data, max_t)
            graphs_acc_speed_track(results_path, best_data, track)
        if gifs:
            p=Process(gifs_acc_speed(results_path, best_data, track))
            p.start()
    # Dados salvos
    if saved_option and saved_data:
        if any(opt in [0, 1, 4, 5] for opt in options):
            graphs_acc_speed_time(results_path, saved_data, max_t_s)
            graphs_acc_speed_track(results_path, saved_data, track)
        if gifs:
            p=Process(gifs_acc_speed(results_path, saved_data, track))
            p.start()

def get_behaviour_data(results_path, filename='best_behaviour.txt'):
    '''
    Reads the txt file and returns the data for the speed and acceleration over time
    '''
    try:
        with open(f'./Neural_Network2/{results_path}/{filename}', 'r') as file:
            linhas = file.readlines()
        data = {}
        max_t = 0
        for linha in linhas[1:]:
            partes = linha.split()
            geracao = int(partes[0])
            t = float(partes[1])
            if t > max_t:
                max_t = t
            dados = np.array([[float(partes[1]), float(partes[2]), float(partes[3]),
                            float(partes[4]), float(partes[5]), float(partes[6])]])    
            if geracao not in data:
                data[geracao] = dados
            else:
                data[geracao] = np.vstack([data[geracao], dados])
        return data, max_t
    except Exception as e:
        print(f'Error while getting behaviour data: {e}')
        return None

#----------------------------------------------#
#          Fitness evolution Plot              #
#----------------------------------------------#
def graph_fitness(results_path, filename='fitness.txt'):
    '''
    Plots the fitness of the best car over the generations
    Default filename is 'fitness.txt'
    '''
    try:
        geracoes = []
        fitness = []
        with open(f'./Neural_Network2/{results_path}/{filename}', 'r') as file:
            linhas = file.readlines()

        for linha in linhas[1:]:
            partes = linha.split()
            geracoes.append(int(partes[0]))
            fitness.append(float(partes[1]))
        # Fitness plot per generation
        plt.figure()
        plt.plot(geracoes, fitness)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.title('Fitness evolution')
        plt.savefig('./Neural_Network2/'+results_path+'/fitness.jpeg', dpi=300, bbox_inches='tight')
    except Exception as e:
        print(f'Error while getting fitness evolution image: {e}')
        return

#----------------------------------------------#
#          Death Points on track Plot          #
#----------------------------------------------#
def graph_crash(results_path, track, filename='deaths.txt'):
    '''
    Plots the crash points on the track
    Default filename is 'deaths.txt'
    '''
    try:
        death_pos = []
        with open(f'./Neural_Network2/{results_path}/{filename}', 'r') as file:
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
        plt.title('Crash Positions on track')
        plt.savefig(f'./Neural_Network2/{results_path}/crash_positions.jpeg', dpi=300, bbox_inches='tight')
    except Exception as e:
        print(f'Error while getting crash on track image: {e}')
        return
    
#-----------------------------------------------------------------------#
#          Acceleration, Steering and Speed Plot over time              #
#-----------------------------------------------------------------------#  
def graphs_acc_speed_time(results_path, data, max_t):
    '''
    Plots the acceleration and speed of the car over time
    Default filename is 'deaths.txt'
    '''
    fig1, (ax1) = plt.subplots(1,1, figsize=(10, 5))
    fig2, (ax2) = plt.subplots(1,1, figsize=(10, 5))
    fig3, (ax3) = plt.subplots(1,1, figsize=(10, 5))
    for gen in data:
        ax1.plot(data[gen][:,0], data[gen][:,2], label=f'{gen}')
        ax2.plot(data[gen][:,0], data[gen][:,1], label=f'{gen}')
        ax3.plot(data[gen][:,0], data[gen][:,3], label=f'{gen}')

        ax1.set_title('Acceleration during simulation time',size=10)
        ax1.set_xlabel('Time (s)',size=10)
        ax1.set_ylabel('Acceleration',size=10)
        ax1.set_xlim(0, max_t)
        ax1.set_ylim(-1.1,1.1)
        fig1.subplots_adjust(hspace=0.3)
        fig1.savefig(f'./Neural_Network2/{results_path}/acc_gen{gen}.jpeg', dpi=300, bbox_inches='tight')
        plt.close(fig1)

        ax2.set_title('Steering during simulation time',size=10)
        ax2.set_xlabel('Time (s)',size=10)
        ax2.set_ylabel('Steering',size=10)
        ax2.set_xlim(0, max_t)
        ax2.set_ylim(-1.1,1.1)
        fig2.subplots_adjust(hspace=0.3)
        fig2.savefig(f'./Neural_Network2/{results_path}/steering_gen{gen}.jpeg', dpi=300, bbox_inches='tight')
        plt.close(fig2)
       
        ax3.set_title('Speed during simulation time',size=10)
        ax3.set_xlabel('Time (s)',size=10)
        ax3.set_ylabel('Velocidade',size=10)
        ax3.set_xlim(0, max_t)
        ax3.set_ylim(0,101)
        fig3.savefig(f'./Neural_Network2/{results_path}/speed_gen{gen}.jpeg', dpi=300, bbox_inches='tight')
        plt.close(fig3)
#----------------------------------------------------------------#
#          Acceleration and Speed Plot on the track              #
#----------------------------------------------------------------#
def graphs_acc_speed_track(results_path, data, track):
    '''
    Plots the acceleration and speed of the car on the track
    '''
    for gen in data:
        dados = data[gen]

        # Dados da melhor trajetória
        x = dados[:,4]  # x position
        y = dados[:,5]  # y position
        acel = dados[:,2]  # acceleration
        speed = dados[:,3]

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        #---------------------------------------------------------#
        #      Plot of acceleration and braking in the track      #
        #---------------------------------------------------------#

        plt.figure()
        plt.imshow(track)
        cmap = plt.get_cmap("jet")
        #norm = PowerNorm(gamma=2, vmin=np.min(acel), vmax=np.max(acel))
        lc = LineCollection(segments, cmap=cmap)
        lc.set_array(acel)
        lc.set_linewidth(2)
        plt.gca().add_collection(lc)

        plt.title(f'Car Trajectory (Best generation: {gen})')
        plt.axis('off')
        plt.colorbar(lc, label="Acceleration")
        plt.savefig(f'./Neural_Network2/{results_path}/track_acc_gen{gen}.jpeg', dpi=300, bbox_inches='tight')
        plt.close()
        #--------------------------------------#
        #      Plot of speed in the track      #
        #--------------------------------------#
        plt.figure()
        plt.imshow(track)
        lc=LineCollection(segments,cmap=cmap)
        lc.set_array(speed)
        lc.set_linewidth(2)
        plt.gca().add_collection(lc)
        plt.title(f'Car Trajectory (Best generation: {gen})')
        plt.axis('off')
        plt.colorbar(lc, label="Speed")
        plt.savefig(f'./Neural_Network2/{results_path}/track_speed_gen{gen}.jpeg', dpi=300, bbox_inches='tight')
        plt.close()

#-----------------------------------------------------------------------------#
#          GIFs of Acceleration and Speed over time on the track              #
#-----------------------------------------------------------------------------#
def gifs_acc_speed(results_path, data, track):
    '''
    Makes gifs of the acceleration and speed of the car over time in the track
    '''
    output_folder = f"./Neural_Network2/{results_path}/frames"
    os.makedirs(output_folder, exist_ok=True)

    cmap = plt.get_cmap("jet")

    for gen in data:
        accel_paths = []
        speed_paths = []

        dados = data[gen]
        x = dados[:, 4]
        y = dados[:, 5]
        acel = dados[:, 2]
        speed = dados[:, 3]
        for i in range(1, len(x)):
            # Points up to i
            angle = math.atan2(y[i] - y[i - 1], x[i] - x[i - 1])
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
            draw_car(plt.gca(), x[i], y[i], angle)
            plt.axis('off')
            plt.title(f"Acceleration - Best Gen: {gen}")
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
            draw_car(plt.gca(), x[i], y[i], angle)
            plt.axis('off')
            plt.title(f"Speed - Best Gen: {gen}")
            plt.colorbar(lc, label="Speed")
            speed_path = f"{output_folder}/speed_{i:04d}.png"
            plt.savefig(speed_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            speed_paths.append(speed_path)

        acc_gif_path = f"./Neural_Network2/{results_path}/trajectory_acceleration_gen{gen}.gif"
        speed_gif_path = f"./Neural_Network2/{results_path}/trajectory_speed_gen{gen}.gif"

        if accel_paths:
            images = [imageio.imread(f) for f in accel_paths]
            imageio.mimsave(acc_gif_path, images, fps=20)

        if speed_paths:
            images = [imageio.imread(f) for f in speed_paths]
            imageio.mimsave(speed_gif_path, images, fps=20)

        # Opcional: limpar os frames
        for f in accel_paths + speed_paths:
            os.remove(f)

def draw_car(ax, x, y, angle, size=10):
    dx = math.cos(angle) * size
    dy = math.sin(angle) * size

    # Triângulo: frente, esquerda, direita
    front = (x + dx, y + dy)
    left = (x + math.cos(angle + math.radians(130)) * size ,
            y + math.sin(angle + math.radians(130)) * size)
    right = (x + math.cos(angle - math.radians(130)) * size,
             y + math.sin(angle - math.radians(130)) * size)

    car_shape = plt.Polygon([front, left, right], color='red')
    ax.add_patch(car_shape)