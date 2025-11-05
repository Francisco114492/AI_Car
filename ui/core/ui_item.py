import pygame

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