class UIManager:
    def __init__(self, items):
        self.items = items  # dict ou lista de Menu

    def handle_events(self, events):
        if self.active_menu:
            self.menus[self.active_menu].handle_events(events)

    def draw(self, screen):
        if self.active_menu:
            self.menus[self.active_menu].draw(screen)