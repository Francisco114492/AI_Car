import math
import numpy as np
from .car_base import CarBase

class Car(CarBase):
    '''
    Simple car class for a car in the game.
    Also has a simple logic for updating position and speed.
    '''
    
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