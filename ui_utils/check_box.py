import pygame

from ui_utils.ui_menu import UiItem

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZENTO = (200, 200, 200)
AZUL_CLARO = (100, 150, 200)

class Checkbox(UiItem):
    def __init__(self, x, y, texto, name=None, group=None, enabled=True):
        super().__init__(x, y, 20, 20, name)
        self.checked = False
        self.texto = texto
        self.group = group
        self.enabled = enabled
        self.font = pygame.font

    def draw(self, screen):
        cor_fundo = BRANCO if self.enabled else CINZENTO
        pygame.draw.rect(screen, cor_fundo, self.rect)
        pygame.draw.rect(screen, PRETO, self.rect, 2)
        if self.checked:
            pygame.draw.line(screen, PRETO, (self.rect.left+3, self.rect.centery), (self.rect.centerx, self.rect.bottom-3), 2)
            pygame.draw.line(screen, PRETO, (self.rect.centerx, self.rect.bottom-3), (self.rect.right-3, self.rect.top+3), 2)
        texto_render = self.font.render(self.texto, True, PRETO)
        screen.blit(texto_render, (self.rect.right + 10, self.rect.top))

    def handle_event(self, event, todos_checkboxes):
        if not self.enabled:
            return  # Se não está ativado, ignora clique!
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
