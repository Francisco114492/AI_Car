import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
import math

image_path = "FIA/Neural_Network/Track3.png"
track = plt.imread(image_path)

inf = {}
max_t = 0
try:
    with open("FIA/txts_/best_behaviour.txt", "r") as file2:
        linhas = file2.readlines()
    for linha in linhas[1:]:
        partes = linha.split()
        geracao = int(partes[0])
        t = float(partes[1])
        if t > max_t:
            max_t = t
        #    tempo    ->       steering    ->    acceleration  ->    speed    ->     pos_x      ->     pos_y
        dados = np.array([[float(partes[1]), float(partes[2]), float(partes[3]), float(partes[4]), float(partes[5]), float(partes[6])]])    
        if geracao not in inf:
            inf[geracao] = dados
        else:
            inf[geracao] = np.vstack([inf[geracao], dados])
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    exit(0)

melhor_geracao = max(inf.keys())
dados = inf[melhor_geracao]

def draw_car(x, y, angle, ax):
    car_size = 5
    front = (x + math.cos(angle) * car_size * 2, y + math.sin(angle) * car_size * 2)
    left = (x + math.cos(angle + math.radians(130)) * car_size,
            y + math.sin(angle + math.radians(130)) * car_size)
    right = (x + math.cos(angle - math.radians(130)) * car_size,
             y + math.sin(angle - math.radians(130)) * car_size)
    triangle = np.array([front, left, right, front])
    return triangle

x = dados[:, 4]  # x position
y = dados[:, 5]  # y position
acel = dados[:, 2]  # acceleration
speed = dados[:, 3]  # speed
angle = np.arctan2(np.diff(y, prepend=y[0]), np.diff(x, prepend=x[0]))

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Colormap
cmap = plt.get_cmap("jet")

# --------------------------------- #
#          Speed animation          #
# --------------------------------- #
fig2, ax2 = plt.subplots()
plt.imshow(track)
plt.title(f'Car Trajectory (Speed) - Best generation: {melhor_geracao}')
plt.axis('off')

lc_speed = LineCollection([], cmap=cmap)
lc_speed.set_array(speed)
lc_speed.set_clim(0, 100)
lc_speed.set_linewidth(2)
ax2.add_collection(lc_speed)

cb2 = plt.colorbar(lc_speed, ax=ax2, label="Speed")

# Car draw
car_plot_speed, = ax2.plot([], [], color='red', linewidth=2)

def update_speed(frame):
    segs = segments[:frame+1]
    lc_speed.set_segments(segs)
    
    # Updates car position
    car_triangle = draw_car(x[frame], y[frame], angle[frame], ax2)
    car_plot_speed.set_data(car_triangle[:, 0], car_triangle[:, 1])  # Updates car on last position
    return lc_speed, car_plot_speed

# Animate the speed on track
ani_speed = FuncAnimation(fig2, update_speed, frames=len(segments), interval=1, blit=True)

# Save as a video
#ani_speed.save('car_trajectory_speed.mp4', writer='ffmpeg', fps=30, dpi=300, extra_args=['-preset', 'slow', '-crf', '18'])

plt.show()
