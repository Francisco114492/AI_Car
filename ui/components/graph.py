import pygame

from ui.core.ui_item import UiItem

class UiGraph(UiItem):
    def __init__(self, x, y, width, height, x_axis_label, y_axis_label, x_axis_range, y_axis_range, data_color=(0,0,0), data_size=100, font_size=16, name=None, visible = True):
        super().__init__(x, y, width, height, name=None, visible = True)
        self.data = []
        self.name = name
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.x_axis_range = x_axis_range
        self.y_axis_range = y_axis_range
        self.data_size = data_size
        self.data_color = data_color
        self.visible = visible
        self.font = pygame.font.SysFont("Arial", font_size)
    
    def add_data(self, x, y):
        self.data.append((x,y))
        if len(self.data) > self.data_size:
            self.data.pop(0)

    def draw(self, screen):
        if not self.visible or not self.data:
            return

        xs, ys = zip(*self.data)

        # --- X RANGE ---
        if isinstance(self.x_axis_range, tuple):
            x_min, x_max = self.x_axis_range
        elif isinstance(self.x_axis_range, str):
            if self.x_axis_range == "dynamic":
                x_min, x_max = min(xs), max(xs)
            elif self.x_axis_range == "window":
                x_max = max(xs)
                x_min = x_max - self.data_size if len(xs) >= self.data_size else min(xs)
            else:
                raise ValueError(f"Invalid x_axis_range: {self.x_axis_range}")
        else:
            raise TypeError("x_axis_range must be tuple or str")

        # --- Y RANGE ---
        if isinstance(self.y_axis_range, tuple):
            y_min, y_max = self.y_axis_range
        elif isinstance(self.y_axis_range, str):
            if self.y_axis_range == "dynamic":
                y_min, y_max = min(ys), max(ys)
            else:
                raise ValueError(f"Invalid y_axis_range: {self.y_axis_range}")
        else:
            raise TypeError("y_axis_range must be tuple or str")

        # evitar divisão por zero
        if x_min == x_max:
            x_min -= 1
            x_max += 1
        if y_min == y_max:
            y_min -= 1
            y_max += 1

        # --- Draw background ---
        pygame.draw.rect(screen, (240, 240, 240), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # --- Transform function ---
        def transform(px, py):
            xn = (px - x_min) / (x_max - x_min)
            yn = (py - y_min) / (y_max - y_min)
            sx = self.rect.x + xn * self.rect.width
            sy = self.rect.y + self.rect.height - yn * self.rect.height
            return (sx, sy)

        # --- Draw data ---
        for i in range(1, len(self.data)):
            p1 = transform(*self.data[i-1])
            p2 = transform(*self.data[i])
            pygame.draw.line(screen, self.data_color, p1, p2, 2)