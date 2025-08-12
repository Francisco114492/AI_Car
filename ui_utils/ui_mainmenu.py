import pygame

from ui_utils.ui_menu import Menu
from Neural_Networks.neural_network import NeuralNetwork
from ui_utils.collapse_button import ColapseButton
from Cars.car import Car


BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)
AZUL_CLARO = (100, 150, 200)

class MainMenu(Menu):
    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.visible = True

        # Título
        self.title_surface = font.render('AI Game', True, PRETO)
        self.title_pos = ((screen.get_width() - self.title_surface.get_width()) // 2,
                          self.title_surface.get_height() + 10)

        # Botões
        nn_options = NeuralNetwork.get_available_networks()
        self.add_item(ColapseButton(90, 60, 200, 60, name="nn_collapsebutton", options=nn_options))

        car_options = Car.get_available_cars()
        self.add_item(ColapseButton(90, 150, 200, 60, name="car_collapsebutton", options=car_options))

    def draw(self):
        if not self.visible:
            return
        self.screen.blit(self.title_surface, self.title_pos)
                # Primeiro, desenha os botões fechados
        for item in self.items:
            if not (isinstance(item, ColapseButton) and item.open):
                item.draw(self.screen)

        # Depois, desenha os que estão abertos por cima de tudo
        for item in self.items:
            if isinstance(item, ColapseButton) and item.open:
                item.draw(self.screen)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            clicked_collapse = None
            for item in self.items:
                if isinstance(item, ColapseButton) and item.rect.collidepoint(mouse_pos):
                    # Fecha todos os outros
                    for other in self.items:
                        if isinstance(other, ColapseButton) and other is not item:
                            other.open = False
                    # Alterna o clicado
                    item.open = not item.open
                    clicked_collapse = item
                    break  # já encontraste o botão clicado, não precisas continuar

        for item in self.items:
            # Só passa o evento se não for o collapse que já trataste acima
            if not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and item is clicked_collapse):
                item.handle_event(event)