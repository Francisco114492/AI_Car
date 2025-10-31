import pygame

from .ui_menu import Menu, UiItem
from ui_utils_t.graph import UiGraph

class UiSimulation(Menu):
    def __init__(self, screen, font, x, y, width, height, car, nn, track, visible=True, test = False):
        super().__init__(screen, font, x, y, width, height, visible)
        self.car = car
        self.nn = nn
        self.track = track
        self.test = test

        # layout: 70% esquerda, 30% direita
        sim_width = int(self.rect.width * 0.7)
        right_width = self.rect.width - sim_width
        sim_height = int(self.rect.height * 0.75)
        bottom_height = self.rect.height - sim_height

        self.simulation_area = pygame.Rect(self.rect.left, self.rect.top, sim_width, sim_height)
        self.bottom_area = pygame.Rect(self.rect.left, self.rect.top + sim_height, sim_width, bottom_height)
        self.right_area = pygame.Rect(self.rect.left + sim_width, self.rect.top, right_width, self.rect.height)

        # container de gráficos no painel direito
        graphs_surface = UiGraphsSurface(self.right_area, max_per_view=3)

        max_speed = car.max_speed if car else 100

        graphs_surface.add_graph(UiGraph(pygame.Rect(0, 0, 0, 0),
                                              "Speed", "Time", "Speed",
                                              "window", (0, max_speed), (0, 0, 255)))
        graphs_surface.add_graph(UiGraph(pygame.Rect(0, 0, 0, 0),
                                              "Acceleration", "Time", "Acc",
                                              "window", (-10, 10), (0, 255, 0)))
        graphs_surface.add_graph(UiGraph(pygame.Rect(0, 0, 0, 0),
                                              "Steering", "Time", "Angle",
                                              "window", (-45, 45), (255, 0, 0)))
        self.add_item(graphs_surface)

    def set_car(self, car):
        self.car = car
        
    def set_nn(self, nn):
        self.nn = nn

    def set_track(self, track):
        self.track = track

    def handle_events(self, event):
        for item in self.items:
            item.handle_event(event)
        self.graphs_surface.handle_events(event)

    def draw(self, screen):
        # fundo
        pygame.draw.rect(screen, (100, 100, 100), self.simulation_area)
        pygame.draw.rect(screen, (80, 80, 80), self.bottom_area)
        pygame.draw.rect(screen, (20, 20, 20), self.right_area)

        for item in self.items:
            item.draw()
        
        if not self.test:
            self.car.draw
            self.nn.draw
  
    
    def forward(self, screen, dt):
        track_img = self.track.png_path
        screen.blit(track_img, self.simulation_area)
        self.car.update(dt, track_img)


class UIGraphsSurface(Menu):
    def __init__(self, screen, font, x, y, width, height, cars, visible=True):
        super().__init__(screen, font, x, y, width, height, visible)
        self.cars = cars

       
class UiGraphsSurface:
    def __init__(self, rect, font, max_per_view=3):
        self.rect = rect
        self.max_per_view = max_per_view
        self.graphs = []
        self.start_index = 0
        self.font = font
        
    def add_graph(self, graph):
        self.graphs.append(graph)

    def handle_events(self, event):
        if len(self.graphs) <= self.max_per_view:
            return
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.start_index = max(self.start_index - self.max_per_view, 0)
            elif event.y < 0:
                self.start_index = min(self.start_index + self.max_per_view,
                                       len(self.graphs) - self.max_per_view)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.start_index = max(self.start_index - self.max_per_view, 0)
            elif event.key == pygame.K_DOWN:
                self.start_index = min(self.start_index + self.max_per_view,
                                       len(self.graphs) - self.max_per_view)

    def draw(self, screen):
        # fundo
        pygame.draw.rect(screen, (50, 50, 50), self.rect)

        # altura de cada gráfico
        if self.max_per_view > 0:
            g_height = self.rect.height // self.max_per_view
        else:
            g_height = self.rect.height

        # desenhar apenas os gráficos visíveis
        for i in range(self.max_per_view):
            idx = self.start_index + i
            if idx >= len(self.graphs):
                break
            graph = self.graphs[idx]
            # atualizar rect do gráfico com base no espaço disponível
            graph.rect = pygame.Rect(
                self.rect.left,
                self.rect.top + i * g_height,
                self.rect.width,
                g_height
            )
            graph.draw(screen, self.font)

    



# import pygame

# from .ui_menu import Menu, UiItem
# from ui_utils.graph import UiGraph

# class UiSimulation(Menu):
#     def __init__(self, screen, font, x, y, width, height, car, nn, track, visible=True):
#         super().__init__(screen, font, x, y, width, height, visible)
#         self.car = car
#         self.nn = nn
#         self.track = track

#         #divide the screen in 3 sections: top left, using almost all the screen, the simulation area, bottom left, something else to define, on the right, the graphs

#         sim_width = int(width * 0.7)   # 70% of width for simulation
#         sim_height = int(height * 0.75) # 75% of height for simulation
#         right_width = width - sim_width
#         bottom_height = height - sim_height

#         # Rectangles for layout
#         simulation_area_rect = pygame.Rect(x, y, sim_width, sim_height)
#         bottom_area_rect = pygame.Rect(x, y + sim_height, sim_width, bottom_height)
#         right_area_rect = pygame.Rect(x + sim_width, y, right_width, height)

#         # Create Surfaces
#         simulation_surface = pygame.Surface((self.simulation_area_rect.width, self.simulation_area_rect.height))
#         bottom_surface = pygame.Surface((self.bottom_area_rect.width, self.bottom_area_rect.height))
#         graph_surface = pygame.Surface((self.right_area_rect.width, self.right_area_rect.height))
        
#         graphs_surface = UiGraphsSurface(
#             screen=self.right_surface,  # desenhará dentro do painel direito
#             font=font,
#             x=0, y=0,  # posições dentro da right_surface
#             width=self.right_area_rect.width,
#             height=self.right_area_rect.height,
#             visible=True,
#             max_per_view=3
#         )


#         max_speed = self.car.max_speed # de futuro aqui deve ter em conta a distancia da pista real, para a tradução em velocidade real
#         speed_graph = UiGraph(
#             graph_surface,
#             font,
#             x=0, y=0,
#             width = graph_surface.get_width(),
#             height = graph_surface.get_height() // 3 - 10,
#             name='Speed Graph',
#             x_axis_label = 'Time(s)',
#             y_axis_label='Speed',
#             x_axis_range='window',
#             y_axis_range=(0,max_speed),
#             data_color=(0,0,255)
#         )

#         acc_graph = UiGraph(
#             graph_surface,
#             font,
#             x=0, y=graph_surface.get_height() // 3 - 10,
#             width = graph_surface.get_width(),
#             height = graph_surface.get_height() // 3 - 10,
#             name='Speed Graph',
#             x_axis_label = 'Time(s)',
#             y_axis_label='Speed',
#             x_axis_range='window',
#             y_axis_range=(0,max_speed),
#             data_color=(0,255,0)
#         )

#         steer_graph = UiGraph(
#             graph_surface,
#             font,
#             x=0, y=2*graph_surface.get_height() // 3 - 10,
#             width = graph_surface.get_width(),
#             height = graph_surface.get_height() // 3 - 10,
#             name='Speed Graph',
#             x_axis_label = 'Time(s)',
#             y_axis_label='Speed',
#             x_axis_range='window',
#             y_axis_range=(0,max_speed),
#             data_color=(255,0,0)
#         )

#         graphs_surface.add_graph(speed_graph, acc_graph, steer_graph)

#         self.add_item(graphs_surface)

#     def draw(self):
#         if not self.visible:
#             return
#         for item in self.items:
#             item.draw()

#     def handle_events(self, event):
#         pass
       
# class UiGraphsSurface:
#     def __init__(self, rect, max_per_view=3):
#         self.rect = rect
#         self.max_per_view = max_per_view
#         self.graphs = []
#         self.start_index = 0
        
#     def add_graph(self, graph):
#         self.graphs.append(graph)

#     def handle_events(self, event):
#         if len(self.graphs) <= self.max_per_view:
#             return
#         if event.type == pygame.MOUSEWHEEL:
#             if event.y > 0:
#                 self.start_index = max(self.start_index - self.max_per_view, 0)
#             elif event.y < 0:
#                 self.start_index = min(self.start_index + self.max_per_view,
#                                        len(self.graphs) - self.max_per_view)
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 self.start_index = max(self.start_index - self.max_per_view, 0)
#             elif event.key == pygame.K_DOWN:
#                 self.start_index = min(self.start_index + self.max_per_view,
#                                        len(self.graphs) - self.max_per_view)

#     def draw(self, screen, font):
#         # fundo
#         pygame.draw.rect(screen, (50, 50, 50), self.rect)

#         # altura de cada gráfico
#         if self.max_per_view > 0:
#             g_height = self.rect.height // self.max_per_view
#         else:
#             g_height = self.rect.height

#         # desenhar apenas os gráficos visíveis
#         for i in range(self.max_per_view):
#             idx = self.start_index + i
#             if idx >= len(self.graphs):
#                 break
#             graph = self.graphs[idx]
#             # atualizar rect do gráfico com base no espaço disponível
#             graph.rect = pygame.Rect(
#                 self.rect.left,
#                 self.rect.top + i * g_height,
#                 self.rect.width,
#                 g_height
#             )
#             graph.draw(screen, font)

# class UiSimulation():
#     def __init__(self, font, x, y, width, height, car, nn, track visible=True):
#         self.font = font
#         self.rect = pygame.Rect(x, y, width, height)
#         self.visible
#         self.car = car
#         self.nn = nn
#         self.track = track
#     def draw(self, screen)

    