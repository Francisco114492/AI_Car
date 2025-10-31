import pygame

from ui_utils.ui_menu import Menu
from neural_networks.neural_network import NeuralNetwork
from ui_utils.collapse_button import ColapseButton
from ui_utils.textbox import TextBox, HiddenLayersTextbox, NumericTextbox
from ui_utils.button import Button
from ui_utils.slider import Slider
from cars.car_base import CarBase
from tracks.track_utils import Track


BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)
AZUL_CLARO = (100, 150, 200)

class MainMenu(Menu):
    def __init__(self, screen, font, x, y, width, height, visible=True):
        super().__init__(screen, font, x, y, width, height, visible)
        self.visible = True

        self.title_surface = font.render('AI Game', True, PRETO)
        self.title_pos = ((screen.get_width() - self.title_surface.get_width()) // 2,
                          self.title_surface.get_height() + 20)

        self.track = None
        self.car = None
        self.nn = None

        nn_list, nn_dict = NeuralNetwork.get_available_networks()
        nn_colapsebutton = ColapseButton(
            90, 90, 200, 60, 
            name="nn_colapsebutton",
            options=nn_dict,
            side = 'front',
            default_text='Selecione uma rede neural: ',
            font_size = 19
            )

        car_list, car_dict = CarBase.get_available_cars()
        car_colapsebutton = ColapseButton(
            90, 180, 200, 60, 
            name="car_colapsebutton", 
            options=car_dict,
            side = 'front',
            default_text='Selecione um carro: ',
            font_size = 20
            )

        tracks_list, tracks_dict = Track.get_tracks()
        track_colapsebutton = ColapseButton(
            90, 270, 200, 60, 
            name = 'track_colapsebutton', 
            options=tracks_dict,
            side = 'front',
            default_text='Selecione uma pista:',
            font_size = 20
            )
        
        alfa_textbox = NumericTextbox(
            450, 90, 100, 30,
            name = 'alfa_textbox',
            font_size = 24,
            default_text = 'Alfa: 0.1',
            visible = False
        )

        mutation_rate_slider = Slider(
            450, 180, 100,
            name = 'mutation_rate_slider',
            min_val = 0.01,
            max_val = 1.0,
            start_val = 0.15,
            visible = False
        )
        
        start_sim_button = Button(
            450, 270, 150, 50,
            text = 'Iniciar Simulação',
            name = 'start_sim_button',
            visible = True,
            font_size = 16,
            active = False
        )

        self.add_item(nn_colapsebutton, car_colapsebutton, track_colapsebutton, alfa_textbox, mutation_rate_slider, start_sim_button)
        # agora alfa e mutation rate serão os parametros a ser definidos pelo utilizador


    def draw(self):
        if not self.visible:
            return
        self.surface.fill(AZUL_CLARO)
        self.surface.blit(self.title_surface, self.title_pos)
                # Primeiro, desenha os botões fechados
        for item in self.items:
            if not (isinstance(item, ColapseButton) and item.open):
                item.draw(self.surface)

        # Depois, desenha os que estão abertos por cima de tudo
        for item in self.items:
            if isinstance(item, ColapseButton) and item.open:
                item.draw(self.surface)

        car_colapsebutton_choice = self.get_item('car_colapsebutton').choice
        nn_colapsebutton_choice = self.get_item('nn_colapsebutton').choice
        track_colapsebutton_choice = self.get_item('track_colapsebutton').choice

        if not nn_colapsebutton_choice == None:
            nn_class = NeuralNetwork.get_nn(nn_colapsebutton_choice)
            nn = nn_class([1,1,1])
            alfa_textbox = self.get_item('alfa_textbox')
            if hasattr(nn, "alfa"):
                alfa_textbox.visible = hasattr(nn, "alfa")
                alfa_textbox.text = str(nn.alfa) 
            
        if not car_colapsebutton_choice == None:
            car = CarBase.get_cars(car_colapsebutton_choice)
            self.get_item('mutation_rate_slider').visible = True

        if not (nn_colapsebutton_choice == None or car_colapsebutton_choice == None or track_colapsebutton_choice == None):
            self.track = Track.get_track(track_colapsebutton_choice)  
            self.car = CarBase.get_car(track_colapsebutton_choice) 
            self.nn = NeuralNetwork.get_nn(track_colapsebutton_choice) 
            self.get_item('start_sim_button').active = True
        self.screen.blit(self.surface, self.surface_pos)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            clicked_collapse = None
            for item in self.items:
                if isinstance(item, ColapseButton) and item.rect.collidepoint(mouse_pos):
                    for other in self.items:
                        if isinstance(other, ColapseButton) and other is not item:
                            other.open = False
                    item.open = not item.open
                    clicked_collapse = item
                    break  
        for item in self.items:
            if not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and item is clicked_collapse):
                item.handle_event(event)
