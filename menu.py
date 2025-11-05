import pygame

from ui.screens.mainmenu import MainMenu
from ui.screens.sim import UiSimulation

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)
AZUL_CLARO = (100, 150, 200)

WIN_WIDTH, WIN_HEIGHT = 1400, 750



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('AI Game - Main Menu')
    font = pygame.font.SysFont("Arial", 36)
    clock = pygame.time.Clock()

    main_menu = MainMenu(screen, font, 0, 0, WIN_WIDTH, WIN_HEIGHT, visible = True)  # cria o menu principal
    sim_menu = UiSimulation(screen, font, 0, 0, WIN_WIDTH, WIN_HEIGHT, car = None, nn = None, track = None, visible = False)

    running = True

    while running:
        screen.fill(AZUL_CLARO)
        main_menu.draw()
        sim_menu.draw()

        
        for event in pygame.event.get():
            start_button=main_menu.get_item('start_sim_button')
            if start_button.handle_event(event) and start_button.visible and main_menu.visible:
                sim_menu.set_car(main_menu.car)
                sim_menu.set_nn(main_menu.nn)
                sim_menu.set_track(main_menu.track)

                main_menu.visible = False
                sim_menu.visible = True
            if event.type == pygame.QUIT:
                running = False
            else:
                main_menu.handle_events(event) if main_menu.visible else None
                sim_menu.handle_events(event) if sim_menu.visible else None


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
