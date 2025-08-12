import pygame


class UiItem:
    _counter = 0
    def __init__(self, x, y, width, height, name=None):
        self.rect = pygame.Rect(x, y, width, height)
        if name is None:
            # uses class name to create a unique name if not provided
            cls = self.__class__
            if not hasattr(cls, '_counter'):
                cls._counter = 0
            cls._counter += 1
            self.name = f"{cls.__name__.lower()}_{cls._counter}"
        else:
            self.name = name

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        self.items = []

    def add_item(self, item):
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
