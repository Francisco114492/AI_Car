import pygame
import os


class UiItem:
    _counter = 0
    def __init__(self, x, y, width, height, name=None, visible = True):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = visible
        if name is None:
            # uses class name to create a unique name if not provided
            cls = self.__class__
            if not hasattr(cls, '_counter'):
                cls._counter = 0
            cls._counter += 1
            self.name = f"{cls.__name__.lower()}_{cls._counter}"
        else:
            self.name = name

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
    
    def draw_img(self, screen):
        if not self.visible:
            return

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
