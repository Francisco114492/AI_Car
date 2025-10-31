import numpy as np
from numba import njit
from .neural_network import NeuralNetwork

class ELU(NeuralNetwork):
    '''
    Exponential Linear Unit (ELU)
    '''
    def __init__(self, layer_sizes, alfa=1):
        super().__init__(layer_sizes)
        self.alfa=alfa

    def __str__(self):
        return (f'''Exponential Linear Unit (ELU) Neural Network with layers {self.layer_sizes} and alfa={self.alfa}
                Description: {self.__doc__}''')

    @njit
    def forward(self, x):
        self.activations = [x]
        self.z_values = []

        a = x
        for i in range(self.num_layers - 1):
            z = np.dot(self.weights[i], a) + self.biases[i]
            self.z_values.append(z)

            if i < self.num_layers - 2:
                a = np.where(z > 0, z, self.alfa * (np.exp(z) - 1))
            else:
                a = np.tanh(z)

            self.activations.append(a)
        return a
    
    def set_alfa(self, alfa):
        self.alfa = alfa