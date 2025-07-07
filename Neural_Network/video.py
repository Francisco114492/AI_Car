import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

# Carregar a imagem da pista
image_path = "FIA/Neural_Network/Track3.png"
track = plt.imread(image_path)

# Variáveis para armazenar os dados
geracoes = []
fitness = []
death_pos = []
alive = []

# Ler os dados do arquivo
with open("FIA/fitness.txt", "r") as file:
    linhas = file.readlines()

for linha in linhas[1:]:  # Pular cabeçalho
    partes = linha.split()
    geracoes.append(int(partes[0]))  # Número da geração
    fitness.append(float(partes[1]))  # Fitness
    death_pos.append([float(partes[2]), float(partes[3])])  # Coordenadas (x, y)
    alive.append(partes[4] == 'True')  # Converter para bool

# Converter listas para arrays NumPy
death_pos = np.array(death_pos)
alive = np.array(alive)

# Criar figura
fig, ax = plt.subplots()
#plt.get_current_fig_manager().window.state('zoomed')
ax.imshow(track)
ax.axis("off")

# Listas para armazenar pontos acumulados ao longo da animação
x_alive, y_alive = [], []
x_dead, y_dead = [], []

# Criar os scatter plots vazios
points_alive, = ax.plot([], [], 'bo', marker='.', label="Vivo")   # Azul (vivos)
points_dead, = ax.plot([], [], 'rx', marker='x', label="Morto")   # Vermelho (mortos)

# Função de atualização da animação
def update(i):
    ax.set_title(f"Geração {geracoes[i]}")

    # Acumular os pontos da geração atual
    if alive[i]:  
        x_alive.append(death_pos[i, 0])
        y_alive.append(death_pos[i, 1])
    else:
        x_dead.append(death_pos[i, 0])
        y_dead.append(death_pos[i, 1])

    # Atualizar os dados do scatter plot
    points_alive.set_data(x_alive, y_alive)
    points_dead.set_data(x_dead, y_dead)

    return points_alive, points_dead

# Criar animação (0.5s entre gerações)
ani = FuncAnimation(fig, update, frames=len(geracoes), interval=1000, repeat=False)

plt.legend()
plt.show()

writer = PillowWriter(fps=100)
ani.save("animacao.gif", writer=writer)
