import pygame


class ButtonDrawer:
    BACKGROUND_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, game_drawer):
        self.game_drawer = game_drawer
        self.buttons = ["Play", "Clear", "Swap", "Pass"]
        self.WIDTH = 2 * self.game_drawer.CELL_SIZE

    def draw_button(self, text, x, y):
        # Draw rectangle behind text
        text_surface, text_rect = self.game_drawer.FONT.render(
            text, self.TEXT_COLOR
        )
        # rect_width = text_rect.width + 10
        rect_width = self.WIDTH
        rect_height = text_rect.height + 10
        rect_x = x - 5
        rect_y = y - 5
        rect = pygame.Rect((rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(
            self.game_drawer.screen,
            self.BACKGROUND_COLOR,
            rect,
        )

        # Draw text
        self.game_drawer.screen.blit(text_surface, (x, y))

        # Add rect to dictionary
        self.game_drawer.button_rects[text] = rect

    def draw(self):
        x_position = 2 * self.game_drawer.BORDER_WIDTH

        for button_text in self.buttons:
            self.draw_button(
                button_text,
                x_position,
                self.game_drawer.HEIGHT
                + 2 * self.game_drawer.CELL_SIZE
                + self.game_drawer.BORDER_WIDTH,
            )
            x_position += (
                self.game_drawer.FONT.size
                + self.WIDTH
                + self.game_drawer.BORDER_WIDTH
            )
