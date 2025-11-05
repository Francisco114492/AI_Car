import pygame

from ui.core.ui_item import UiItem


class Slider(UiItem):
    def __init__(self, x, y, width, name=None, min_val=0, max_val=1, start_val=0.5, step=0.01, visible=True, font_size = 24):
        super().__init__(x, y, width, 10, name, visible)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.value = start_val
        self.dragging = False
        self.handle_radius = 8
        self.font = pygame.font.SysFont("Arial", font_size)
        self.update_handle_pos()

    def update_handle_pos(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + int(ratio * self.rect.width)

    def draw(self, screen):
        if not self.visible:
            return
        # Draw line
        pygame.draw.line(screen, (200, 200, 200), (self.rect.x, self.rect.centery),
                         (self.rect.right, self.rect.centery), 3)
        # Draw handle
        pygame.draw.circle(screen, (100, 100, 255), (self.handle_x, self.rect.centery), self.handle_radius)
        
        # Optional: show value
        val_text = self.font.render(f"{self.value:.2f}", True, (255, 255, 255))
        screen.blit(val_text, (self.rect.right + 10, self.rect.y - 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.handle_x - self.handle_radius, self.rect.centery - self.handle_radius,
                           self.handle_radius * 2, self.handle_radius * 2).collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Clamp within the slider
                self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.right))
                # Convert position to value
                ratio = (self.handle_x - self.rect.x) / self.rect.width
                raw_value = self.min_val + ratio * (self.max_val - self.min_val)
                # Snap to step
                self.value = round(raw_value / self.step) * self.step
