import numpy as np

from Neural_Network import NeuralNetwork

class ReLU(NeuralNetwork):
    def forward(self, x):
        z1 = np.dot(self.W1, x) + self.b1
        a1 = np.maximum(0, z1)  # ReLU
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = np.tanh(z2) # tanh for output in range (-1, 1)
        return a2
    def forward(self, x):
        self.activations = [x] # used for drawing the neural network, stores the arrays
        self.z_values = []

        a = x
        for i in range(self.num_layers - 1):
            z = np.dot(self.weights[i], a) + self.biases[i]
            self.z_values.append(z)

            if i < self.num_layers - 2:
                a = np.maximum(0, z)
            else:
                a = np.tanh(z) # tanh for output in range (-1, 1)
            self.activations.append(a)
        return a