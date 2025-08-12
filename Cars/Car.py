import math
import numpy as np
import pygame
import inspect

class Car:
    def __init__(self, x, y, angle, neural_net, sensors_angles=[], car_size=5, max_speed=5, color = (0,0,0), finish_color = (0,255,0)):
        '''
        Initializes all the car variables
        '''
        # car variables for each iteration
        self.x = x
        self.y = y
        self.angle = angle  # angle 
        self.speed = 0 # speed

        # global variables
        self.sensors = sensors_angles # dict with the angles of the sensors and each distance associated 
        self.car_size = car_size # car size for drawing
        self.max_speed = max_speed
        self.bound_color = color
        self.finish_line_color = finish_color

        # variables for tests or evaluation
        self.distance = 0  # a measure used for fitness (distance traveled)
        self.network = neural_net

        # variables for simulation
        self.output = []
        self.alive = True
        self.finished = False

    def sense(self, track):
        """
        Cast rays (sensors) at several angles relative to the car's heading.
        The sensor returns a normalized distance (0 to 1) before a boundary (black pixel)
        is encountered.
        """
        sensor_data = []
        for s_angle, s_dist in self.sensors:
            angle = self.angle + s_angle
            distance = 0 
            while distance < s_dist:
                test_x = int(self.x + math.cos(angle) * distance)
                test_y = int(self.y + math.sin(angle) * distance)
                # If the sensor goes out of bounds, stop
                if test_x < 0 or test_x >= track.get_width() or test_y < 0 or test_y >= track.get_height():
                    break
                color = track.get_at((test_x, test_y))
                # Stop if we hit the color defined as boundary pixel
                if color[:3] == self.bound_color:
                    break
                distance += 1
            sensor_data.append(distance / s_dist)  # normalize the reading
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
        if color[:3] == self.bound_color:
            return True
        return False

    def check_finish(self, track):
        '''
        Checks if a car has reached the finish line.
        Returns True or False.
        '''
        if self.x < 0 or self.x >= track.get_width() or self.y < 0 or self.y >= track.get_height():
            return False
        pixel = track.get_at((int(self.x), int(self.y)))
        finish_color = self.finish_line_color
        return pixel[:3] == finish_color
       
    def forward(self, track, dt,sim_time, sensors, surface=None):
        '''
        Updates the car based on the outputs of steering and acceleration
        '''
        if not self.alive:
            return
        
        # Obtain sensor inputs from the environment
        inputs = np.array(sensors).reshape(-1, 1)
        if surface:
            self.network.draw(surface, inputs)
        # Returns the output based on the input
        outputs = self.network.forward(inputs)
        self.output.append([sim_time,outputs[0,0],outputs[1,0],self.speed,self.x,self.y])

        self.update(outputs, dt)

        # Check for collision
        if self.check_collision(track):
            self.alive = False
        
        # Check if the car has reached the finish line
        if self.check_finish(track):
            self.alive = False
            self.finished = True

    def update(self, input, dt):
        '''
        # Two Neural Network outputs:
        # outputs[0]: steering command (negative: left, positive: right)
        # outputs[1]: acceleration command (negative: decelerate, positive: accelerate)
        # keeps record of the position and outputs given to the vehicle
        # '''
        # Update the car's angle and speed based on outputs
        steering = input[0, 0]
        accel_signal = input[1, 0]
        turn_rate = 0.2 - (self.speed/800)  # scaling factor for turning
        self.angle += steering * turn_rate
        
        acceleration = accel_signal * 100  # scaling factor for acceleration
        self.speed += acceleration * dt
        self.speed *= 0.99  # apply simple friction
        # Clamp speed to the range [0, max_speed]
        self.speed = max(self.max_speed/2, min(self.speed, self.max_speed))
        
        # Update position and accumulate distance traveled
        prev_x, prev_y = self.x, self.y
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        self.distance += math.hypot(self.x - prev_x, self.y - prev_y)
        
    def get_car_vertices(self):
        front = (
            self.x + math.cos(self.angle) * self.car_size * 2,
            self.y + math.sin(self.angle) * self.car_size * 2
        )
        left = (
            self.x + math.cos(self.angle + math.radians(130)) * self.car_size,
            self.y + math.sin(self.angle + math.radians(130)) * self.car_size
        )
        right = (
            self.x + math.cos(self.angle - math.radians(130)) * self.car_size,
            self.y + math.sin(self.angle - math.radians(130)) * self.car_size
        )
        return [front, left, right]
    
    def draw(self, screen, track):
        '''
        Draw the car as a rotated triangle pointing in the direction of travel.
        '''
        vertex=self.get_car_vertices()
        pygame.draw.polygon(screen, (255, 0, 0), vertex)
        # Optionally, draw sensor rays for visualization
        sensors = self.sense(track)
        for distance_norm, s_angle in sensors:
            distance = distance_norm * self.sensors[s_angle]
            end_x = self.x + math.cos(self.angle + s_angle) * distance
            end_y = self.y + math.sin(self.angle + s_angle) * distance
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (end_x, end_y), 1)

    @classmethod
    def get_available_cars(cls):
        cars = {}
        name = cls.__name__
        doc = inspect.getdoc(cls) or None
        cars[name] = doc
        for subclass in cls.__subclasses__():
            name = subclass.__name__
            doc = inspect.getdoc(subclass) or None
            cars[name] = doc
        return cars
