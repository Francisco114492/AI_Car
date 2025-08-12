import pygame

import Cars 
import Neural_Networks
from ui_utils.ui_mainmenu import MainMenu
from ui_utils.collapse_button import ColapseButton
from ui_utils.button import Button
from ui_utils.textbox import TextBox, NumericTextbox
from ui_utils.slider import Slider
from ui_utils.check_box import Checkbox

from Neural_Networks.neural_network import NeuralNetwork
from Cars.car import Car

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)
AZUL_CLARO = (100, 150, 200)

WIN_WIDTH, WIN_HEIGHT = 1400, 750



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('AI Game - Main Menu')
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    main_menu = MainMenu(screen, font)  # cria o menu principal
    running = True

    while running:
        screen.fill(AZUL_CLARO)
        main_menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                main_menu.handle_events(event)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def simulation(screen, font, test=False):
    pygame.display.set_caption('AI Game - Simulation')


main()
