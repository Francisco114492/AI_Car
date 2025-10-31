import math
import pygame
import inspect

class CarBase:
    '''
    Simple car class for a car in the game.
    Also has a simple logic for updating position and speed.
    '''

    cars_list = []
    cars_dict = {}

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
        self.input_size = len(sensors_angles)
        self.output_size = 2

        # variables for tests or evaluation
        self.distance = 0  # a measure used for fitness (distance traveled)
        self.network = neural_net

        # variables for simulation
        self.output = []
        self.alive = True
        self.finished = False

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
    
    def __str__(self):
        return f'''Car object:
    car_size: {self.car_size}
    max_speed: {self.max_speed}
    sensors angles: {list(self.sensors.keys())}
    Bound color: {self.bound_color}
    Finish line color: {self.finish_line_color}
Neural Network: {self.network}
'''
    
    def __lt__(self, other): # the comparison of cars is now based on distance traveled
        return self.distance < other.distance

    def __eq__(self, other):
        return self.distance == other.distance

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
        cls.cars_list = []
        cls.cars_dict = {}
        for subclass in cls.__subclasses__():
            name = subclass.__name__
            doc = inspect.getdoc(subclass) or None
            cls.cars_dict[name] = doc
            cls.cars_list.append(subclass)
        return cls.cars_list, cls.cars_dict
    
    @classmethod
    def get_car(cls, name):
        for subclass in cls.cars_list:
            if subclass.__name__ == name:
                return subclass
        return None