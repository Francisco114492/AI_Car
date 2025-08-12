import numpy as np

from .neural_network import NeuralNetwork

class LeakyReLU(NeuralNetwork):
    '''
    Leaky ReLU activation function for neural networks.
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
                a = np.where(z > 0, z, self.alfa * z)
            else:
                a = np.tanh(z) # tanh for output in range (-1, 1)

            self.activations.append(a)
        return a