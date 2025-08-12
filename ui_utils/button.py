import pygame

from ui_utils.ui_menu import UiItem

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)

class Button(UiItem):
    def __init__(self, x, y, width, height, text, name=None, active=False):
        super().__init__(x, y, width, height, name)
        self.text = text
        self.active = active

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        cor = CINZENTO if self.active else BRANCO
        pygame.draw.rect(screen, cor, (self.x, self.y, self.width, self.height))
        mensagem = font.render(self.text, True, PRETO)
        screen.blit(mensagem, (self.x + 10, self.y + 15))
        
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            if click[0] == 1:
                return True
        return False
    
    def change_text(self, new_text):
        self.text = new_text

    def change_active(self, new_active=None):
        if new_active is not None:
            self.active = new_active
        else:
            self.active = not self.active

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True