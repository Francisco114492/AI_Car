import pygame
from ui.core.ui_item import UiItem

class Menu:
    def __init__(self, screen, font, x, y, width, height, visible):
        self.screen = screen
        self.font = font
        self.visible: bool = visible
        self.items: list[UiItem] = []
        self.surface = pygame.Surface((width, height))
        self.surface_pos = (x, y)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
    
    def add_item(self, *items):
        for item in items:
            if item not in self.items:
                self.items.append(item)

    def draw(self):
        if not self.visible:
            return
        for item in self.items:
            item.draw(self.screen)

    def handle_events(self, event):
        if not self.visible:
            return
        for item in self.items:
            item.handle_event(event)

    def get_item(self, name):
        for item in self.items:
            if getattr(item, "name", None) == name:
                return item
        return None
