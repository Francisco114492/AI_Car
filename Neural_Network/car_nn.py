import pygame
import numpy as np
import math
import os

# ----------------------------- #
#       General variables       #
# ----------------------------- #

MAX_SPEED=100 # car's max speed
WIDTH = 10 # car dimensions
HEIGHT = 5
CAR_SIZE = 5
SENSOR_DISTANCE=40 # maximum sensor range in pixels
SENSOR_ANGLES = [-math.pi/2,-math.pi/4, -math.pi/8, 0, math.pi/8, math.pi/4,math.pi/2]
#ALFA = 0.2 # 0.5, 1.0, 1.5, 2.0        #ELU
            # 0.01, 0.05, 0.1, 0.2, 0.3 #ReLU
POPULATION_SIZE=30
#MUTATION_RATE = 0.15  # adjust mutation intensity

# ---------------------------------------------------------- #
# Define the starting position and orientation for all cars. #
#                Adjust to your track design                 #
# ---------------------------------------------------------- #

TRACK_PATHS=["images/Track1.png","images/Track2.png","images/Track3.png","images/Track4.png","images/Track5.png"]
SCREEN_STATS=[[1400,800],[1400,800],[900,500],[3808,2674],[1024,1024]] # width and height of the screen for each track
WIN_WIDTH, WIN_HEIGHT = 700, 700
# Zoom area around the best car
ZOOM_STATS=[(400, 400),(400, 400),(400, 400),(400, 400),(400, 400)]
# size of the minimap
MM_STATS=[(400, 300),(400, 300),(400, 300),(400, 300),(400, 300)]
START_POS=[[100,500],[120,100],[645,445],[708,2261],[521,249]] # starting position of the car for each track
START_ANGLES=[0,math.pi/2,-3*math.pi/4,-3*math.pi/4,math.pi/4] # starting angle of the car for each track

# ----------------------------- #
# Neural Network Implementation #
# ----------------------------- #
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Save dimensions so that we can use them later (e.g., in copying)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        # Initialize weights and biases randomly
        self.W1 = np.random.randn(hidden_size, input_size)
        self.b1 = np.random.randn(hidden_size, 1)
        self.W2 = np.random.randn(output_size, hidden_size)
        self.b2 = np.random.randn(output_size, 1)
    
    def forward(self, x):
        z1 = np.dot(self.W1, x) + self.b1
        a1 = np.where(z1 > 0, z1, 0.5 * (np.exp(z1) - 1))  # ELU
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = np.tanh(z2)  # outputs in roughly the range (-1, 1)
        return a2
    
    def mutate(self, rate):
        '''
        Applies the mutation rate given and adds some randomness
        '''
        # Simply add gaussian noise to weights and biases
        self.W1 += np.random.randn(*self.W1.shape) * rate
        self.b1 += np.random.randn(*self.b1.shape) * rate
        self.W2 += np.random.randn(*self.W2.shape) * rate
        self.b2 += np.random.randn(*self.b2.shape) * rate

    
    def copy(self):
        '''
        Returns a copy of the network.
        '''
        # Create and return a deep copy of this network
        copy_net = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        copy_net.W1 = np.copy(self.W1)
        copy_net.b1 = np.copy(self.b1)
        copy_net.W2 = np.copy(self.W2)
        copy_net.b2 = np.copy(self.b2)
        return copy_net
    
    def draw(self, surface, input_vector):
        surface.fill((255, 255, 255))  # Clear the surface
        largura, altura = surface.get_size()
        layer_spacing = 130  # Reduzido para caber melhor na nn_surface
        node_radius = 10

        # Ativações
        z1 = np.dot(self.W1, input_vector) + self.b1
        #a1 = np.where(z1 > 0, z1, ALFA * (np.exp(z1) - 1))  # ELU
        a1 = np.tanh(z1)
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = np.tanh(z2)

        activations = [input_vector.flatten(), a1.flatten(), a2.flatten()]
        layers = [self.input_size, self.hidden_size, self.output_size]
        positions = []

        font = pygame.font.SysFont(None, 16)

        all_weights = np.concatenate((self.W1.flatten(), self.W2.flatten()))
        min_w = np.min(all_weights)
        max_w = np.max(all_weights)
        for i, num_nodes in enumerate(layers):
            layer_pos = []
            x = 50 + i * layer_spacing
            total_height = num_nodes * (node_radius * 2 + 6)
            y_start = (altura - total_height) // 2

            for j in range(num_nodes):
                y = y_start + j * (node_radius * 2 + 6)
                pos = (x, y)
                layer_pos.append(pos)

                # Nó
                pygame.draw.circle(surface, (0, 0, 0), pos, node_radius, 1)
                val = activations[i][j]
                label = font.render(f"{val:.1f}", True, (0, 0, 0))
                if i==0:
                    surface.blit(label, (x - node_radius - label.get_width() - 6, y - 8))
                else:
                    surface.blit(label, (x + node_radius + 2, y - 8))
            positions.append(layer_pos)

        def weight_to_color(weight, min_weight=-1, max_weight=1):
            max_abs = max(abs(min_weight), abs(max_weight))
            normalized = weight / max_abs
            normalized = max(-1, min(1, normalized))  # clamp to [-1, 1]

            if normalized < 0:
                # Negative: interpolate from white to red
                intensity = int((1 + normalized) * 255)  # normalized in [-1,0] => [0,1]
                return (255, intensity, intensity)  # red to white
            else:
                # Positive: interpolate from white to blue
                intensity = int((1 - normalized) * 255)  # normalized in [0,1] => [1,0]
                return (intensity, intensity, 255)  # white to blue
        
        # Input -> Hidden
        for i, start in enumerate(positions[0]):
            for j, end in enumerate(positions[1]):
                w = self.W1[j][i]
                if w!=0:
                    color = weight_to_color(w, min_w, max_w)
                    width = max(1, int(min(abs(w) * 3, 2)))
                    pygame.draw.line(surface, color, start, end, width)
                else:
                    pygame.draw.line(surface, (255,255,255), start, end, width)

        # Hidden -> Output
        for i, start in enumerate(positions[1]):
            for j, end in enumerate(positions[2]):
                w = self.W2[j][i]
                color = weight_to_color(w, min_w, max_w)
                width = max(1, int(min(abs(w) * 3, 2)))
                pygame.draw.line(surface, color, start, end, width)


# ------------------------------ #
#   Car (Agent) Implementation   #
# ------------------------------ #
class Car:
    def __init__(self, x, y, angle, neural_net):
        '''
        Initializes all the car variables
        '''
        self.x = x
        self.y = y
        self.angle = angle  # in radians; 0 means facing straight
        self.speed = 0
        self.alive = True
        self.finished = False
        self.distance = 0  # a measure of fitness (distance traveled)
        self.network = neural_net
        self.output = []

    def sense(self, track):
        """
        Cast rays (sensors) at several angles relative to the car's heading.
        The sensor returns a normalized distance (0 to 1) before a boundary (black pixel)
        is encountered.
        """
        sensor_data = []
        for s_angle in SENSOR_ANGLES:
            angle = self.angle + s_angle
            distance = 0
            while distance < SENSOR_DISTANCE:
                test_x = int(self.x + math.cos(angle) * distance)
                test_y = int(self.y + math.sin(angle) * distance)
                # If the sensor goes out of bounds, stop
                if test_x < 0 or test_x >= track.get_width() or test_y < 0 or test_y >= track.get_height():
                    break
                color = track.get_at((test_x, test_y))
                # Stop if we hit a black pixel (boundary)
                if color[:3] == (0, 0, 0):
                    break
                distance += 1
            sensor_data.append(distance / SENSOR_DISTANCE)  # normalize the reading
        return sensor_data

    def check_collision(self, track):
        '''
        Checks if a car has hit a wall.
        Returns True or False.
        '''
        # If the car's center is outside bounds or is over a black pixel, it collides.
        if self.x < 0 or self.x >= track.get_width() or self.y < 0 or self.y >= track.get_height():
            return True
        color = track.get_at((int(self.x), int(self.y)))
        if color[:3] == (0, 0, 0):
            return True
        return False

    def check_finish(self, track):
        '''
        Checks if a car has reached the finish line.
        Returns True or False.
        '''
        # In this example, the finish line is defined by green pixels.
        if self.x < 0 or self.x >= track.get_width() or self.y < 0 or self.y >= track.get_height():
            return False
        pixel = track.get_at((int(self.x), int(self.y)))
        finish_color = (0, 255, 0)
        return pixel[:3] == finish_color
       
    def update(self, track, dt,sim_time, sensors, sensors_before, surface=None):
        '''
        Updates the car based on the outputs of steering and acceleration
        '''
        if not self.alive:
            return
        
        # Obtain sensor inputs from the environment
        #sensor=np.concatenate((sensors, sensors_before))
        inputs = np.array(sensors).reshape(-1, 1)
        if surface:
            self.network.draw(surface, inputs)
        # Returns the output based on the input
        outputs = self.network.forward(inputs)
        # Two outputs:
        # outputs[0]: steering command (negative: left, positive: right)
        # outputs[1]: acceleration command (negative: decelerate, positive: accelerate)
        # keeps record of the position and outputs given to the vehicle
        self.output.append([sim_time,outputs[0,0],outputs[1,0],self.speed,self.x,self.y])
        steering = outputs[0, 0]
        accel_signal = outputs[1, 0]
        
        # Update the car's angle and speed based on outputs
        turn_rate = 0.2 - (self.speed/800)  # scaling factor for turning
        self.angle += steering * turn_rate
        
        acceleration = accel_signal * 100  # scaling factor for acceleration
        self.speed += acceleration * dt
        self.speed *= 0.99  # apply simple friction
        # Clamp speed to the range [0, max_speed]
        self.speed = max(MAX_SPEED/2, min(self.speed, MAX_SPEED))
        
        # Update position and accumulate distance traveled
        prev_x, prev_y = self.x, self.y
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        self.distance += math.hypot(self.x - prev_x, self.y - prev_y)
        
        # Check for collision
        if self.check_collision(track):
            self.alive = False
        
        # Check if the car has reached the finish line
        if self.check_finish(track):
            self.alive = False
            self.finished = True

    def draw(self, screen, track):
        '''
        Draw the car as a rotated triangle pointing in the direction of travel.
        '''
        # Determine three points for the triangle.
        front = (self.x + math.cos(self.angle) * CAR_SIZE * 2,
                 self.y + math.sin(self.angle) * CAR_SIZE * 2)
        left = (self.x + math.cos(self.angle + math.radians(130)) * CAR_SIZE,
                self.y + math.sin(self.angle + math.radians(130)) * CAR_SIZE)
        right = (self.x + math.cos(self.angle - math.radians(130)) * CAR_SIZE,
                 self.y + math.sin(self.angle - math.radians(130)) * CAR_SIZE)
        pygame.draw.polygon(screen, (255, 0, 0), [front, left, right])
        # Optionally, draw sensor rays for visualization
        sensors = self.sense(track)
        for distance_norm, s_angle in zip(sensors, SENSOR_ANGLES):
            distance = distance_norm * SENSOR_DISTANCE
            end_x = self.x + math.cos(self.angle + s_angle) * distance
            end_y = self.y + math.sin(self.angle + s_angle) * distance
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (end_x, end_y), 1)

# ------------------------------------------ #
#    Writing in files for later analysis     #
# ------------------------------------------ #

def write_file(filename, header, data):
    headers=["Generation  Pos_x  Pos_y\n",
             "Generation  Tempo  Steering  Acceleration  Speed  Pos_x  Pos_y\n",
             f"Generations  Fitness\n"] #\n{SENSOR_ANGLES} {SENSOR_DISTANCE}
    formats = [
        "{0} {1:.2f} {2:.2f}\n",
        "{0} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}\n",
        "{0} {1:.2f}\n"
    ]
    ### TEST
    if filename=="fitness_comp_leaky_ReLU.txt" or filename=="fitness_comp_ELU.txt" or filename == "fitness_comp_tanh.txt":
        with open(filename, "a") as file:
            file.write(headers[header])
            fmt = formats[header]
            for row in data:
                file.write(fmt.format(*row))
        return 
    ### TEST
    with open(filename, "w") as file:
        file.write(headers[header])
        fmt = formats[header]
        for row in data:
            file.write(fmt.format(*row))
    

# -------------------------------------------------- #
#     Handle game events, like clicks on button      #
# -------------------------------------------------- #

def handle_events(cars, running, sim_duration, to_save, track_n, screen, mut):
    for event in pygame.event.get():
        if event.type == pygame.RESIZABLE:
            # Resize the screen to fit the new window size
            screen.fill((100, 150, 200))
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            for car in cars: # End simulation
                car.alive=False
            running = False
            main(track_n, mut)  # Restart whole simulation
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            for car in cars: # Restart all cars and go into next generation
                car.alive = False 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            sim_duration += 5 # Increase simulation time
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            sim_duration -= 5 # Decrease simulation time
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for car in cars: # End simulation
                car.alive=False
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        #safe exit from the simulation, after generation time ends or all cars die, it exits simulation
            if running==False:
                running=True
            else:
                running=False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            # saves the best car of this generation
            if to_save==True:
                to_save=False
            else:
                to_save=True
    return cars, running, sim_duration, to_save, screen

# ------------------------- #
#   Fitness Evaluation      #
# ------------------------- #

def calc_fitness(cars, track, cache_fitness, sim_time, best_distance):
    # Evaluation: choose the best car based on distance traveled;
    # award an extra bonus if a car finished (reached the green finish line).
    generation_best_car = None
    generation_best_fitness = -float('inf')
    for car in cars:
        fitness = car.distance + cache_fitness
        if car.distance>2500: # bonus for being fast
            fitness+=car.distance/2500*50000/sim_time
        if car.check_collision(track):
            fitness -= 750  # extra penalty for collision
        if car.check_finish(track): 
            fitness+=1000 # bonus for finishing the track
        if fitness > generation_best_fitness: #keep record of the car with best fitness
            generation_best_fitness = fitness
            generation_best_car = car
    # to save the case where the car reached the furthest
    if generation_best_car.distance>best_distance:
        best_distance=generation_best_car.distance
    return generation_best_car, generation_best_fitness, best_distance

# ----------------------------- #
#   Main Simulation & GA Loop   #
# ----------------------------- #
#def main(track_n, W1, b1, W2, b2, function, alfa):
def main(track_n, mutation):

    global MUTATION_RATE

    MUTATION_RATE=mutation
    ### TEST 
    pygame.init()

    largura, altura = 1400, 750
    screen = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
    screen.fill((100, 150, 200))
    ### TEST
    
    track_path=TRACK_PATHS[track_n]
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_STATS[track_n]
    START_X, START_Y = START_POS[track_n]
    START_ANGLE = START_ANGLES[track_n]
    ZOOM_WIDTH, ZOOM_HEIGHT = ZOOM_STATS[track_n]
    MM_WIDTH, MM_HEIGHT = MM_STATS[track_n]
    
    pygame.display.set_caption("Neural Car Race")
    clock = pygame.time.Clock()

    map = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    nn_surface = pygame.Surface((400, 400))
    nn_surface.fill((255,255,255))
    
    # Load the track image.
    # The image must include black boundaries and a green finish line.
    try:
        track = pygame.image.load(track_path).convert()
    except Exception as e:
        print("Error loading track.png. Please ensure it is in the current directory.")
        return

    # Genetic Algorithm Parameters
    generation = 0
    cars = []
    input_size = len(SENSOR_ANGLES)#*2  # seven sensor readings
    hidden_size = 20
    output_size = 2  # one output for steering, one for acceleration
    # Create the initial population
    for _ in range(POPULATION_SIZE):
        nn = NeuralNetwork(input_size, hidden_size, output_size)
        car = Car(START_X, START_Y, START_ANGLE, nn)
        cars.append(car)
        sensors_before=car.sense(track)
    generation_best_car = None
    best_network = None
    best_fitness = -float('inf')
    best_distance= -float('inf')
    primeira_curva = -float('inf')
    running = True
    sim_duration = 60 # run each generation for up to 60 seconds
    generation_best_fitness=0
    save_arr=[]
    fitness_arr=[]
    deaths_arr=[]
    best_car_arr = []

    while running and generation < 20:
        generation += 1
        print(f"Generation {generation}")
        sim_time = 0
        total_steps=0
        cache_fitness=0
        to_save=False
        # Simulation loop for current generation.
        while sim_time < sim_duration and any(car.alive for car in cars):
            dt = clock.tick(60) / 1000.0  # frame time in seconds
            sim_time += dt
            total_steps+=1
            cars, running, sim_duration, to_save, screen=handle_events(cars, running, sim_duration, to_save, track_n, screen, mutation)

            # Find the best car in the current generation
            best_car_dist = max(cars, key=lambda c: c.distance if c.alive==True else -float('inf'))
            zoom_area = pygame.Rect( # zoom around the best car
                best_car_dist.x - ZOOM_WIDTH // 2,
                best_car_dist.y - ZOOM_HEIGHT//2,
                ZOOM_WIDTH, ZOOM_HEIGHT
                )
            map.blit(track, (0, 0))
            zoom_area.clamp_ip(map.get_rect())
            zoom_surface=map.subsurface(zoom_area)
            for car in cars:
                if car.alive:
                    sensors=car.sense(track)
                    if sensors[3]>0.9 and car.speed>=0.9*MAX_SPEED:
                        cache_fitness+=0.5
                    if car == best_car_dist:
                        car.update(track, dt,sim_time, sensors, sensors_before, nn_surface)
                    else:
                        car.update(track, dt,sim_time, sensors, sensors_before)
                    car.draw(map, track)
                    sensors_before=sensors

            minimap = pygame.transform.scale(map, (MM_WIDTH, MM_HEIGHT))
            largura, altura = screen.get_size()

            zoom_map = pygame.transform.scale(zoom_surface, (WIN_WIDTH, WIN_HEIGHT))

            # We show on the screen the max time, the current time, generation and fitness of last generation
            zoom_width, zoom_height = zoom_map.get_size()
            font=pygame.font.SysFont('Times New Roman',15)
            info=font.render(f"Tempo Máximo: {sim_duration:.1f}s Tempo:{sim_time:.1f}s Geração:{generation}",True,(0,0,0))
            zoom_map.blit(info,(10,10))
            info2=font.render(f"Fitness:{generation_best_fitness:.2f}",True,(0,0,0))
            zoom_map.blit(info2,(10,30))
            if running==False:
                # print on screen some info (if the q button is on and it will exit at the end)
                info4=font.render(f"Exiting",True,(255,0,0))
                map.blit(info4,(zoom_width-50,10))
            if to_save==True:
                # print on screen if the best car of the generation is gonna be saved (by hitting s)
                info3=font.render(f"Saving best car of generation",True,(0,255,0))
                zoom_map.blit(info3,(zoom_width/2-15,10))
            
            mm_larg, mm_alt = minimap.get_size()
            nn_img_larg, nn_img_alt = nn_surface.get_size()
            screen.blit(minimap, ( (largura - mm_larg -20, altura - mm_alt - 20)))
            screen.blit(zoom_map, (10, 10))
            #nn_surface_zoomed = pygame.transform.scale(nn_surface, (400, 400))
            nn_img_larg, nn_img_alt = nn_surface.get_size()
            screen.blit(nn_surface,( (largura - nn_img_larg -20, 20)))
            pygame.display.flip()

       
       # calculate fitness of the cars
        generation_best_car, generation_best_fitness,best_distance=(
        calc_fitness(cars, track, cache_fitness, sim_time, best_distance)
        )
        
        fitness_arr.append((generation,generation_best_fitness))
        print(f"Best Fitness for Generation {generation}: {generation_best_fitness:.2f}")

        # Update the overall best network
        if generation_best_fitness > best_fitness:
            if primeira_curva == -float('inf') and generation_best_fitness > 0:
                primeira_curva = generation
            best_car_arr=[]
            best_fitness = generation_best_fitness
            gen_best_fit= generation
            best_network = generation_best_car.network.copy()

        for car in cars:
            if car.alive==False:
                # save the last position of all the crashed cars
                deaths_arr.append((generation,car.x,car.y))

        # save the cars that are supposed to be saved (by hitting s)
        for row in generation_best_car.output:
            expanded_row = [generation] + row
            best_car_arr.append(expanded_row)
        if to_save == True:
            save_arr.append(best_car_arr)
        # Generate new population using the best network from the current generation,
        # applying mutation to introduce variation.
        new_cars = []
        for _ in range(POPULATION_SIZE):
            if best_network is not None:
                child_network = best_network.copy()
            else:
                child_network = NeuralNetwork(input_size, hidden_size, output_size)
            child_network.mutate(MUTATION_RATE)
            new_car = Car(START_X, START_Y, START_ANGLE, child_network)
            new_cars.append(new_car)
        cars = new_cars
    
    txt_path = "results" + str(track_n+1)
    # Garante que a pasta existe
    os.makedirs("Neural_Network/"+txt_path, exist_ok=True)
    write_file("Neural_Network/"+txt_path+"/deaths.txt",0,deaths_arr) # save the crash positions of all the cars
    write_file("Neural_Network/"+txt_path+"/best_behaviour.txt",1,best_car_arr) # save the best behaviour of the car that did the most distance in all the generations
    write_file("Neural_Network/"+txt_path+"/save_behaviour.txt",1,save_arr) # save the best behaviour of the car that did the most distance is the generations chosen by the user (by hitting s)
    write_file("Neural_Network/"+txt_path+"/fitness.txt",2,fitness_arr) # save the fitness of the best car for each generations
    #write_file("test2.txt",2,fitness_arr)
    ### TEST
    n_crash= len(deaths_arr)
    return n_crash, best_fitness, primeira_curva, gen_best_fit, generation_best_car.network.W1, generation_best_car.network.b1, generation_best_car.network.W2, generation_best_car.network.b2
