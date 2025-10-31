import pygame

from ui_utils.ui_menu import UiItem

class ColapseButton(UiItem):
    def __init__(self, x, y, width, height, name=None, options=None, open=False, default_text="Selecione...    ↘", side = 'below', max_visible=5, font_size = 24):
        super().__init__(x, y, width, height, name)
        self.open = open
        self.choice = None
        self.options = options if options else {}
        self.font = pygame.font.SysFont("Arial", font_size)
        self.option_height = 30
        self.default_text = default_text
        self.scroll_offset = 0
        self.max_visible = max_visible  # Máx de opções visíveis ao mesmo tempo
        self.draw_side = side

    def add_option(self, name, description):
        self.options[name] = description

    def draw(self, screen, surf_rect=None):
        if not self.visible:
            return
        # Botão principal
        pygame.draw.rect(screen, (70, 70, 200), self.rect)
        header_str = "Menu [-]" if self.open else (self.choice or self.default_text)
        header_text = self.font.render(header_str, True, (255, 255, 255))
        screen.blit(header_text, (self.rect.x + 5, self.rect.y + 5))

        # Opções abertas
        if self.open:
            self.draw_options(screen)

    def draw_options(self, screen, surf_rect=None):
        mouse_pos = pygame.mouse.get_pos()
        hover_desc = None

        # Calcular deslocamento
        if self.draw_side == "below":
            base_x = self.rect.x
            base_y = self.rect.y + self.rect.height
        elif self.draw_side == "front":
            base_x = self.rect.x + self.rect.width
            base_y = self.rect.y
        else:
            base_x, base_y = self.rect.x, self.rect.y + self.rect.height  # fallback

        # Calcular opções visíveis
        visible_items = list(self.options.items())[self.scroll_offset:self.scroll_offset + self.max_visible]

        for i, (name, desc) in enumerate(visible_items):
            y_pos = base_y + i * self.option_height
            option_rect = pygame.Rect(base_x, y_pos, self.rect.width, self.option_height)
            color = (100, 100, 250) if option_rect.collidepoint(mouse_pos) else (50, 50, 150)
            pygame.draw.rect(screen, color, option_rect)
            option_text = self.font.render(name, True, (255, 255, 255))
            screen.blit(option_text, (option_rect.x + 5, y_pos + 5))
            if option_rect.collidepoint(mouse_pos):
                hover_desc = desc

        # Mostrar descrição
        if hover_desc:
            lines = self.wrap_text(hover_desc, self.rect.width, max_lines=3)
            line_height = self.font.get_height()
            desc_height = line_height * len(lines) + 10
            desc_rect = pygame.Rect(base_x, y_pos + self.option_height, self.rect.width, desc_height)
            pygame.draw.rect(screen, (0, 0, 0), desc_rect)
            for i, line in enumerate(lines):
                desc_text = self.font.render(line, True, (255, 255, 255))
                screen.blit(desc_text, (desc_rect.x + 5, desc_rect.y + 5 + i*line_height))
                
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Clique no botão principal
            if self.rect.collidepoint(mouse_pos):
                self.open = not self.open
                return None

            # Clique nas opções
            if self.open:
                # Calcular deslocamento com base na posição de desenho
                if self.draw_side == "below":
                    base_x = self.rect.x
                    base_y = self.rect.y + self.rect.height
                elif self.draw_side == "front":
                    base_x = self.rect.x + self.rect.width
                    base_y = self.rect.y
                else:
                    base_x, base_y = self.rect.x, self.rect.y + self.rect.height  # fallback

                visible_items = list(self.options.items())[self.scroll_offset:self.scroll_offset + self.max_visible]
                for i, (name, desc) in enumerate(visible_items):
                    y_pos = base_y + i * self.option_height
                    option_rect = pygame.Rect(base_x, y_pos, self.rect.width, self.option_height)
                    if option_rect.collidepoint(mouse_pos):
                        self.choice = name
                        self.open = False
                        return name

        # Scroll do rato
        if event.type == pygame.MOUSEWHEEL and self.open:
            total_options = len(self.options)
            max_scroll = max(0, total_options - self.max_visible)
            self.scroll_offset = max(0, min(self.scroll_offset - event.y, max_scroll))

        return None


    def wrap_text(self, text, max_width, max_lines=3):
        words = text.split()
        lines = []
        current_line = ""
        font = self.font
        word_index = 0
        total_words = len(words)

        while word_index < total_words:
            word = words[word_index]
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
                word_index += 1
            else:
                lines.append(current_line)
                current_line = ""
                if len(lines) == max_lines - 1:
                    # Estamos na penúltima linha, para aqui para truncar depois
                    break

        # Se sobrou linha em construção e ainda não atingiu o limite
        if current_line and len(lines) < max_lines:
            lines.append(current_line)

        # Se ainda há palavras por processar (texto sobrando), significa que tem que truncar
        if word_index < total_words:
            last_line = lines[-1]
            # Corta o último caractere até caber as reticências
            while font.size(last_line + "...")[0] > max_width and len(last_line) > 0:
                last_line = last_line[:-1]
            lines[-1] = last_line + " ..."

        return lines