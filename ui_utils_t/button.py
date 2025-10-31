import pygame

from ui_utils_t.ui_menu import UiItem

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)

class Button(UiItem):
    def __init__(self, x, y, width, height, text, name=None, active=False, visible=True, font_size = 24):
        super().__init__(x, y, width, height, name, visible)
        self.text = text
        self.active = active
        self.font = pygame.font.SysFont("Arial", font_size)

    def draw(self, screen):
        if not self.visible:
            return
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        cor = BRANCO if self.active else CINZENTO
        pygame.draw.rect(screen, cor, self.rect)
        mensagem = self.font.render(self.text, True, PRETO)
        text_width, text_height = self.font.size(self.text)
        text_x = self.rect.x + (self.rect.width - text_width) // 2
        text_y = self.rect.y + (self.rect.height - text_height) // 2
        screen.blit(mensagem, (text_x, text_y))
        
        if self.rect.x + self.rect.width > mouse[0] > self.rect.x and self.rect.y + self.rect.height > mouse[1] > self.rect.y:
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

    def handle_event(self, event):
        if not self.active or not self.visible:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False