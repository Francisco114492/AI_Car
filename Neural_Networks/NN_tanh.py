import numpy as np

from .neural_network import NeuralNetwork

class tanh(NeuralNetwork):
    def forward(self, x):
        self.activations = [x]
        self.z_values = []

        a = x
        for i in range(self.num_layers - 1):
            z = np.dot(self.weights[i], a) + self.biases[i]
            self.z_values.append(z)

            a = np.tanh(z) # tanh for output in range (-1, 1)

            self.activations.append(a)
        return a