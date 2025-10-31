import pygame
import time

from ui_utils.ui_menu import UiItem


class TextBox(UiItem):
    def __init__(self, x, y, width, height, name=None, font_size=24, max_chars=20, default_text='', visible=True):
        super().__init__(x, y, width, height, name, visible)
        self.color_inactive = (200, 200, 200)
        self.color_active = (255, 255, 255)
        self.color_border = (100, 100, 255)
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text = ''
        self.active = False
        self.cursor_visible = True
        self.last_cursor_toggle = time.time()
        self.max_chars = max_chars
        self.default_text = default_text
        self.cursor_index = len(self.text)  # posição no texto, não em px!
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_LEFT:
                if self.cursor_index > 0:
                    self.cursor_index -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_index < len(self.text):
                    self.cursor_index += 1
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_index > 0:
                    self.text = self.text[:self.cursor_index - 1] + self.text[self.cursor_index:]
                    self.cursor_index -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_index < len(self.text):
                    self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]
            

    def update(self):
        if time.time() - self.last_cursor_toggle >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = time.time()

    def draw(self, screen):
        if not self.visible:
            return
        # Draw background
        pygame.draw.rect(screen, self.color_active if self.active else self.color_inactive, self.rect)
        pygame.draw.rect(screen, self.color_border, self.rect, 2)

        # Render text
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - txt_surface.get_height()) // 2))

        # Draw cursor
        if self.active and self.cursor_visible:
            self.cursor_x = self.rect.x + 5 + txt_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_height = self.rect.height - 10
            pygame.draw.line(screen, (0, 0, 0), (self.cursor_x, cursor_y), (self.cursor_x, cursor_y + cursor_height), 2)


class NumericTextbox(TextBox):
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN and self.active:
            if event.unicode.isnumeric() or event.unicode in ['.', ',']:
                self.text = self.text[:self.cursor_index] + event.unicode + self.text[self.cursor_index:]
                self.cursor_index += 1
        

class HiddenLayersTextbox(NumericTextbox):
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.text = self.text[:self.cursor_index] + ',' + self.text[self.cursor_index:]
                    self.cursor_index += 1
