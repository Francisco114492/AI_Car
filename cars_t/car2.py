from .car_base import CarBase
from .car1 import Car

COEF=0.2

class Car2(Car, CarBase):
    '''
    Test car (not working)
    '''
    def __init__(self, atrito):
        super().__init__()
        self.atrito = atrito
    
    def __str__(self):
        base_str  = super().__str__()
        return f'''{base_str} 
    Atrito= {self.atrito}'''

    def update():

        pass

