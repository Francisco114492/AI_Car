import pygame
import numpy as np
import math
import random
import sys
from collections import defaultdict
import time
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# Parameters and Constants
# ----------------------------------------

# Window
#WINDOW_WIDTH = 900
#WINDOW_HEIGHT = 500
#TRACK_IMAGE = "FIA/Track3.png"

# Q-Learning hyper parameters
ALPHA = 0.1           # Learning rate
GAMMA = 0.95          # Discount factor
EPSILON = 1.0         # Starting exploration rate
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01

# Main program parameters
NUM_EPISODES = 20000
NUM_LAPS = 2               # Car considers job done after reaching the given number of laps
MAX_STEPS = NUM_LAPS*680   # One lap has around 680 steps

NUM_ACTIONS = 5       # 0: turn hard left, 1: turn soft left, 2: go straight
                      # 3: turn hard right, 4: turn soft right

# Track parameters
TRACK_PATHS=["images/Track1.png","images/Track2.png","images/Track3.png"]
SCREEN_STATS=[[1400,800],[1400,800],[900,500]] # width and height of the screen for each track
START_POS=[[100,500],[120,100],[645,445]] # starting position of the car for each track
START_ANGLES=[0,math.pi/2,-3*math.pi/4] # starting angle of the car for each track

# Sensor parameters
SENSOR_ANGLES = [math.radians(-90), math.radians(-45), 0, math.radians(45), math.radians(90)]  # relative angles from car's current angle
MAX_SENSOR_DISTANCE = 100
SENSOR_BINS = 5      # Number of discrete bins per sensor

# Car movement parameters
SPEED = 4                     # Pixels per update
TURN_ANGLE = math.radians(15) # Turning angle per update (in radians)
CAR_SIZE = 10                 # Used for drawing the car

# Starting position and orientation

#START_ANGLE = math.radians(45)  # Facing downward
#START_ANGLE = math.radians(-135)  # Facing upnward

# ----------------------------------------
# Car Class with Sensor-based Q-Learning
# ----------------------------------------
class Car:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def update(self, action):
        """
        Update the car's orientation and position based on the chosen action.
        Actions:
        """
        if action == 0:   # Hard left
            self.angle -= TURN_ANGLE
        elif action == 1: # Soft left
            self.angle -= TURN_ANGLE/2

        # Action 2 would be for Straight

        elif action == 3: # Soft right
            self.angle += TURN_ANGLE/2
        elif action == 4:   # Hard right
            self.angle += TURN_ANGLE

        # Move forward along the current orientation
        self.x += math.cos(self.angle) * SPEED
        self.y += math.sin(self.angle) * SPEED

    def cast_ray(self, sensor_angle, track):
        """
        Cast a ray in direction (self.angle + sensor_angle) until hitting a black pixel
        or reaching MAX_SENSOR_DISTANCE. Returns the measured distance.
        """
        global_angle = self.angle + sensor_angle
        for distance in range(1, MAX_SENSOR_DISTANCE):
            # Compute the point along the ray
            rx = int(self.x + math.cos(global_angle) * distance)
            ry = int(self.y + math.sin(global_angle) * distance)
            # If out of window boundaries, return the distance
            if rx < 0 or rx >= SCREEN_WIDTH or ry < 0 or ry >= SCREEN_HEIGHT:
                return distance
            # Check the color at the ray's point
            color = track.get_at((rx, ry))[:3]
            if color == (0, 0, 0):  # Black is the track's limit
                return distance
        return MAX_SENSOR_DISTANCE

    def get_sensor_state(self, track):
        """
        Returns a tuple of discretized sensor readings.
        For each sensor (left, center, right): the raw distance is binned into SENSOR_BINS.
        """
        readings = []
        bin_size = MAX_SENSOR_DISTANCE / SENSOR_BINS
        for sensor_angle in SENSOR_ANGLES:
            raw_distance = self.cast_ray(sensor_angle, track)
            # Discretize the sensor reading
            bin_val = int(raw_distance / bin_size)
            if bin_val >= SENSOR_BINS:
                bin_val = SENSOR_BINS - 1 # Ensures the binned value doesn’t exceed the maximum allowed
            readings.append(bin_val)
        return tuple(readings)

    def check_collision(self, track):
        """
        Checks if the car's center has collided with the track limit (i.e., a black pixel)
        """
        color = track.get_at((int(self.x), int(self.y)))[:3]
        return color == (0, 0, 0)
    
    def check_finish(self, track):
        """
        Checks if the car's center has reached the finish line (i.e., a green pixel)
        """
        color = track.get_at((int(self.x), int(self.y)))[:3]
        return color == (0, 255, 0)

    def draw(self, screen):
        """
        Draw the car as a rotated triangle pointing in the direction of travel.
        """
        # Determine three points for the triangle
        front = (self.x + math.cos(self.angle) * CAR_SIZE * 2,
                 self.y + math.sin(self.angle) * CAR_SIZE * 2)
        left = (self.x + math.cos(self.angle + math.radians(130)) * CAR_SIZE,
                self.y + math.sin(self.angle + math.radians(130)) * CAR_SIZE)
        right = (self.x + math.cos(self.angle - math.radians(130)) * CAR_SIZE,
                 self.y + math.sin(self.angle - math.radians(130)) * CAR_SIZE)
        pygame.draw.polygon(screen, (255, 0, 0), [front, left, right])

# -------------------------------------------------- #
#     Handle game events, like clicks on button      #
# -------------------------------------------------- #

def handle_events(running, track_n, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            main(track_n, screen)  # Restart whole simulation
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        #safe exit from the simulation, after generation time ends or all cars die, it exits simulation
            if running==False:
                running=True
            else:
                running=False
    return running

# ----------------------------------------
# Main Q-Learning and Simulation Loop
# ----------------------------------------
def main(track_n,screen):
    global EPSILON, track_path, SCREEN_WIDTH, SCREEN_HEIGHT, START_X, START_Y, START_ANGLE
    track_path=TRACK_PATHS[track_n]
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_STATS[track_n]
    START_X, START_Y = START_POS[track_n]
    START_ANGLE = START_ANGLES[track_n]
    #pygame.init()
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Q-Learning Car on Loaded Track")
    clock = pygame.time.Clock()

    # Load and scale the track image
    track = pygame.image.load(track_path).convert()
    track = pygame.transform.scale(track, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize Q-table as a defaultdict that returns a zero vector for unseen states.
    # Ensures that whenever a new state is encountered, it initializes a zero vector.
    # Otherwise it's needed to specify np.zeros() at every state update (not optimal because of redundancy)
    Q_table = defaultdict(lambda: np.zeros(NUM_ACTIONS))

    best_path = []  # Stores the path of the best reward episode
    best_ouputs = [] # Only stores steering (hard left, left, straight, right, hard right) in radians because speed is constant 
    best_reward = float('-inf')  # Start with the lowest possible reward

    start_time = time.time()

    rewards = []

    collision = []

    for episode in range(1, NUM_EPISODES + 1):
        # Reset the car for a new episode.
        car = Car(START_X, START_Y, START_ANGLE)
        state = car.get_sensor_state(track)
        total_reward = 0
        path = []  # Track the current episode's path
        output = [] # Track the current outputs
        done = False
        finished=False

        for step in range(1, MAX_STEPS + 1):
            # Process events (so the window stays responsive)
            done=handle_events(done, track_n, screen)
            # ---------- Epsilon-Greedy Action Selection ----------
            if random.random() < EPSILON:
                action = random.randint(0, NUM_ACTIONS - 1)
            else:
                action = int(np.argmax(Q_table[state]))

            # ---------- Take Action ----------
            init_steer = car.angle
            car.update(action)
            final_steer = car.angle
            path.append((car.x, car.y))  # Store the car's position
            output.append((step, final_steer-init_steer))   # Store the car's steering


            # Check for collisions.
            if car.check_collision(track):
                reward = -100  # Heavy penalty for going off track
                collision.append((car.x,car.y))
                done = True    # Once hit, restart the car
            elif car.check_finish(track):
                reward = 100   # If there is a finish line (marked as green) it's strongly rewarded
                done = True    # Once finished go again
                finished=True
            else:
                reward = 1     # Reward for a safe time step
                next_state = car.get_sensor_state(track) # Save the best state that didn't go off track

            # ---------- Q-Learning Update ----------
            best_next = np.argmax(Q_table[next_state])
            Q_table[state][action] += ALPHA * (reward + GAMMA * best_next - Q_table[state][action])

            state = next_state
            total_reward += reward


            # ---------- Visualization ----------
            # It's shown as a continuation from the last best try (after collision).
            # It prefered that way for simplcity, instead of watching best tries individualy each time
            if total_reward > best_reward:
                screen.blit(track, (0, 0))
                car.draw(screen)

                # Draw sensor rays.
                for sensor_angle in SENSOR_ANGLES:
                    d = car.cast_ray(sensor_angle, track)
                    end_x = car.x + math.cos(car.angle + sensor_angle) * d
                    end_y = car.y + math.sin(car.angle + sensor_angle) * d
                    pygame.draw.line(screen, (0, 255, 0), (car.x, car.y), (end_x, end_y), 1) # Green rays

                best_reward = total_reward  # Update the best reward
                best_path = path.copy()     # Keep track of all best paths
                best_ouputs = output.copy() # Keep track of all best ouputs

                # Display some info.
                font = pygame.font.SysFont("Arial", 20)
                info = font.render(f"Episode: {episode}  Step: {step}  Best reward: {best_reward}", True, (255, 0, 255))
                screen.blit(info, (10, 10))
                pygame.display.flip()
                clock.tick(30)  # Limit rendering to 30 FPS

            if done:
                break
            
    
        rewards.append((episode, total_reward)) # Store all rewards per episode

        # Decay epsilon for less exploration over time.
        EPSILON = max(MIN_EPSILON, EPSILON * EPSILON_DECAY)
        print(f"Episode {episode} ended at step {step} with total reward {total_reward}, epsilon: {EPSILON:.3f}")
    
        if step == MAX_STEPS or finished:
            break

    rewards.append((episode, total_reward)) # Store the last reward after completion

    end_time = time.time() # Time spent for the program to finish all episodes

    execution_time = end_time - start_time
    print(f"Time spent: {execution_time:.2f}s")

    # ----------------------------------------
    # Plot the Q-table in 3D
    # ----------------------------------------

    states = list(Q_table.keys())
    q_values = np.array([Q_table[s] for s in states])   

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    states_idx = np.arange(len(states))
    actions_idx = np.arange(q_values.shape[1])

    X, Y = np.meshgrid(states_idx, actions_idx)
    Z = np.array(q_values).T  # Transpose to match dimensions

    ax.plot_surface(X, Y, Z, cmap="coolwarm")

    ax.set_xlabel("State Index")
    ax.set_ylabel("Action")
    ax.set_zlabel("Q-Value")
    ax.set_title("Q-Table 3D Visualization")

    # ----------------------------------------
    # Saving useful information
    # ----------------------------------------

    # Save the best path to a file
    with open("Q-learning/resultados/best_path.txt", "w") as f1:
        for x, y in best_path:
            f1.write(f"{x:.2f},{y:.2f}\n")
    print(f"Best path saved with reward: {best_reward}")

    # Save the steer outputs from the best path to a file
    with open("Q-learning/resultados/best_outputs.txt", "w") as f2:
        for num, steer in best_ouputs:
            f2.write(f"{num},{steer:.3f}\n")

    # Save all rewards from each episode
    with open("Q-learning/resultados/all_rewards.txt", "w") as f3:
        for ep, r in rewards:
            f3.write(f"{ep},{r}\n")

    # Save collision locations
    with open("Q-learning/resultados/collisions.txt", "w") as f4:
        for x_col, y_col in collision:
            f4.write(f"{x_col:.2f},{y_col:.2f}\n")
    return
#plt.show()

#if __name__ == "__main__":
    #main()
    #with open('FIA/Q-learning/view_path.py') as file1:
        #exec(file1.read())
    #with open('view_output_and_rewards.py') as file2:
        #exec(file2.read())
    #with open('view_collisions.py') as file3:
        #exec(file3.read())
