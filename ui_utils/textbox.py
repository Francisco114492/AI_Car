import pygame
import time

from ui_utils.ui_menu import UiItem


class TextBox(UiItem):
    def __init__(self, x, y, width, height, name=None, font_size=24, max_chars=20):
        super().__init__(x, y, width, height, name)
        self.color_inactive = (200, 200, 200)
        self.color_active = (255, 255, 255)
        self.color_border = (100, 100, 255)
        self.font = pygame.font.SysFont(None, font_size)
        self.text = ''
        self.active = False
        self.cursor_visible = True
        self.last_cursor_toggle = time.time()
        self.cursor_interval = 0.5
        self.max_chars = max_chars

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print("Texto inserido:", self.text)  # Ou outro comportamento
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_chars:
                self.text += event.unicode

    def update(self):
        # Alternar cursor a piscar
        if time.time() - self.last_cursor_toggle >= self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = time.time()

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, self.color_active if self.active else self.color_inactive, self.rect)
        pygame.draw.rect(screen, self.color_border, self.rect, 2)

        # Render text
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - txt_surface.get_height()) // 2))

        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + txt_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_height = self.rect.height - 10
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)


class NumericTextbox(TextBox):
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.text += ','
            elif event.unicode.isnumeric() or event.unicode in ['.', ',']:
                self.text += event.unicode