import numpy as np

from .neural_network import NeuralNetwork

class sigmoid(NeuralNetwork):
    '''
    Sigmoid neural network class.
    Last layer is a tanh for output in range -1, 1.
    '''
    def forward(self, x):
        z1 = np.dot(self.W1, x) + self.b1
        a1 = np.sigmoid(z1)
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = 2* np.sigmoid(z2) - 1
        return a2
    def forward(self, x):
        self.activations = [x]
        self.z_values = []

        a = x
        for i in range(self.num_layers - 1):
            z = np.dot(self.weights[i], a) + self.biases[i]
            self.z_values.append(z)

            if i < self.num_layers - 2:
                a = np.sigmoid(z)
            else:
                a = 2 * np.tanh(z) -1 
            # alternative to tanh for output in range (-1, 1)
            self.activations.append(a)
        return a