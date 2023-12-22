import pygame


class CurrentMoveDrawer:
    def __init__(self, game_drawer):
        self.game_drawer = game_drawer

    def draw(self, player):
        # Assuming player.current_move is the dictionary representing the move
        for tile, (x, y) in player.current_move.items():
            # Create a rectangle for the tile
            rect = pygame.Rect(
                self.game_drawer.BORDER_WIDTH + x * self.game_drawer.CELL_SIZE,
                self.game_drawer.BORDER_WIDTH
                + (self.game_drawer.board.HEIGHT - 1 - y)
                * self.game_drawer.CELL_SIZE,
                self.game_drawer.CELL_SIZE,
                self.game_drawer.CELL_SIZE,
            )

            # # Draw the rectangle with a different color to highlight it
            # pygame.draw.rect(
            #     self.game_drawer.screen,
            #     self.game_drawer.HIGHLIGHT_COLOR,  # Define this color in your __init__ method
            #     rect,
            #     3,  # Increase border width to make it more noticeable
            # )

            pygame.draw.rect(
                self.game_drawer.screen,
                tile.BASE_COLOR,
                rect,
            )

            # Draw border
            pygame.draw.rect(
                self.game_drawer.screen,
                self.game_drawer.BORDER_COLOR,
                rect,
                1,
            )

            # Add drawn tile to dictionary so it can be clicked
            self.game_drawer.tile_rects[tile] = rect

            # Add text if necessary
            text_surface, rect = self.game_drawer.FONT.render(
                str(tile), tile.TEXT_COLOR
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
            self.game_drawer.screen.blit(text_surface, (text_x, text_y))
