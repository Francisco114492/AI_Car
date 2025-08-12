import numpy as np
from numba import njit
from .neural_network import NeuralNetwork

class ELU(NeuralNetwork):
    '''
    Exponential Linear Unit (ELU)
    '''
    def __init__(self, layer_sizes, alfa):
        super().__init__(self, layer_sizes)
        self.alfa=alfa

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
                a = np.tanh(z) # tanh for output in range (-1, 1)

            self.activations.append(a)
        return a