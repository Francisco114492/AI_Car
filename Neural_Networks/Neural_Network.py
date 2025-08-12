import numpy as np
import pygame
import inspect

class NeuralNetwork:
    def __init__(self, layer_sizes, weights=None, biases=None):
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)

        self.weights = weights if weights is not None else [
            np.random.randn(out_size, in_size)
            for in_size, out_size in zip(layer_sizes[:-1], layer_sizes[1:])
        ]
        self.biases = biases if biases is not None else [
            np.random.randn(size, 1) for size in layer_sizes[1:]
        ]

    def mutate(self, rate):
        '''
        Applies the mutation rate given and adds some randomness
        '''
        for i in range(len(self.weights)):
            self.weights[i] += np.random.randn(*self.weights[i].shape) * rate
            self.biases[i] += np.random.randn(*self.biases[i].shape) * rate

    @staticmethod
    def create(layer_sizes, seed=None):
        if seed is not None:
            np.random.seed(seed)
        weights = [
            np.random.randn(out_size, in_size)
            for in_size, out_size in zip(layer_sizes[:-1], layer_sizes[1:])
        ]
        biases = [
            np.random.randn(size, 1)
            for size in layer_sizes[1:]
        ]
        return weights, biases


    def copy(self):
        '''
        Returns a copy of the network.
        '''
        # Create and return a deep copy of this network
        copy_net = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        copy_net.W1 = np.copy(self.W1)
        copy_net.b1 = np.copy(self.b1)
        copy_net.W2 = np.copy(self.W2)
        copy_net.b2 = np.copy(self.b2)
        return copy_net
    
    def draw(self, surface, input_vector):
        surface.fill((255, 255, 255))  # Clear the surface
        largura, altura = surface.get_size()
        layer_spacing = 130  # Reduzido para caber melhor na nn_surface
        node_radius = 10

        # Ativações
        z1 = np.dot(self.W1, input_vector) + self.b1
        a1 = np.tanh(z1)
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = np.tanh(z2)

        activations = [input_vector.flatten(), a1.flatten(), a2.flatten()]
        layers = [self.input_size, self.hidden_size, self.output_size]
        positions = []

        font = pygame.font.SysFont(None, 16)

        all_weights = np.concatenate((self.W1.flatten(), self.W2.flatten()))
        min_w = np.min(all_weights)
        max_w = np.max(all_weights)
        for i, num_nodes in enumerate(layers):
            layer_pos = []
            x = 50 + i * layer_spacing
            total_height = num_nodes * (node_radius * 2 + 6)
            y_start = (altura - total_height) // 2

            for j in range(num_nodes):
                y = y_start + j * (node_radius * 2 + 6)
                pos = (x, y)
                layer_pos.append(pos)

                # Nó
                pygame.draw.circle(surface, (0, 0, 0), pos, node_radius, 1)
                val = activations[i][j]
                label = font.render(f"{val:.1f}", True, (0, 0, 0))
                if i==0:
                    surface.blit(label, (x - node_radius - label.get_width() - 6, y - 8))
                else:
                    surface.blit(label, (x + node_radius + 2, y - 8))
            positions.append(layer_pos)

        def weight_to_color(weight, min_weight=-1, max_weight=1):
            max_abs = max(abs(min_weight), abs(max_weight))
            normalized = weight / max_abs
            normalized = max(-1, min(1, normalized))  # clamp to [-1, 1]

            if normalized < 0:
                # Negative: interpolate from white to red
                intensity = int((1 + normalized) * 255)  # normalized in [-1,0] => [0,1]
                return (255, intensity, intensity)  # red to white
            else:
                # Positive: interpolate from white to blue
                intensity = int((1 - normalized) * 255)  # normalized in [0,1] => [1,0]
                return (intensity, intensity, 255)  # white to blue
        
        # Input -> Hidden
        for i, start in enumerate(positions[0]):
            for j, end in enumerate(positions[1]):
                w = self.W1[j][i]
                if w!=0:
                    color = weight_to_color(w, min_w, max_w)
                    width = max(1, int(min(abs(w) * 3, 2)))
                    pygame.draw.line(surface, color, start, end, width)
                else:
                    pygame.draw.line(surface, (255,255,255), start, end, width)

        # Hidden -> Output
        for i, start in enumerate(positions[1]):
            for j, end in enumerate(positions[2]):
                w = self.W2[j][i]
                color = weight_to_color(w, min_w, max_w)
                width = max(1, int(min(abs(w) * 3, 2)))
                pygame.draw.line(surface, color, start, end, width)

    @classmethod
    def get_available_networks(cls):
        networks = {}
        for subclass in cls.__subclasses__():
            name = subclass.__name__
            doc = inspect.getdoc(subclass) or None
            networks[name] = doc
        return networks
