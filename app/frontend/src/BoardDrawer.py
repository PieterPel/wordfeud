import pygame


class BoardDrawer:
    def __init__(self, game_drawer):
        self.game_drawer = game_drawer

    def draw(self):
        # Fill the background
        self.game_drawer.screen.fill(self.game_drawer.BACKGROUND_COLOR)

        # Draw the border
        pygame.draw.rect(
            self.game_drawer.screen,
            self.game_drawer.BORDER_COLOR,
            pygame.Rect(
                0,
                0,
                self.game_drawer.WIDTH + 2 * self.game_drawer.BORDER_WIDTH,
                self.game_drawer.HEIGHT
                + 3 * self.game_drawer.CELL_SIZE
                + 2 * self.game_drawer.BORDER_WIDTH,
            ),
            self.game_drawer.BORDER_WIDTH,
        )

        # Draw the board
        for y in range(self.game_drawer.board.HEIGHT):
            for x in range(self.game_drawer.board.LENGTH):
                cell = self.game_drawer.board[x, y]

                if cell.tile:
                    base_color = cell.tile.BASE_COLOR
                    text_color = cell.tile.TEXT_COLOR
                    text = str(cell.tile)
                else:
                    base_color = cell.base_color
                    text_color = cell.TEXT_COLOR
                    text = cell.multiplier

                # Render the cell
                rect = pygame.Rect(
                    self.game_drawer.BORDER_WIDTH
                    + x * self.game_drawer.CELL_SIZE,
                    self.game_drawer.BORDER_WIDTH
                    + (self.game_drawer.board.HEIGHT - 1 - y)
                    * self.game_drawer.CELL_SIZE,
                    self.game_drawer.CELL_SIZE,
                    self.game_drawer.CELL_SIZE,
                )

                pygame.draw.rect(self.game_drawer.screen, base_color, rect)

                # Draw border
                pygame.draw.rect(
                    self.game_drawer.screen,
                    self.game_drawer.BORDER_COLOR,
                    rect,
                    1,
                )

                # Add empty cell rect to list
                if not cell.tile:
                    self.game_drawer.coordinates_empty_cells[(x, y)] = rect

                # Add text if necessary
                if not text == "":
                    text_surface, rect = self.game_drawer.FONT.render(
                        text, text_color
                    )
                    text_x = (
                        self.game_drawer.BORDER_WIDTH
                        + x * self.game_drawer.CELL_SIZE
                        + (self.game_drawer.CELL_SIZE - rect.width) / 2
                    )
                    text_y = (
                        self.game_drawer.BORDER_WIDTH
                        + (self.game_drawer.board.HEIGHT - 1 - y)
                        * self.game_drawer.CELL_SIZE
                        + (self.game_drawer.CELL_SIZE - rect.height) / 2
                    )
                    self.game_drawer.screen.blit(
                        text_surface, (text_x, text_y)
                    )
