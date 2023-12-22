import pygame


class PlankDrawer:
    def __init__(self, game_drawer):
        self.game_drawer = game_drawer

    def draw(self, player):
        # Draw the plank
        for i, tile in enumerate(player.plank):
            tile_x = (
                self.game_drawer.BORDER_WIDTH + i * self.game_drawer.CELL_SIZE
            )
            tile_y = (
                self.game_drawer.HEIGHT + 2 * self.game_drawer.BORDER_WIDTH
            )
            rect = pygame.Rect(
                tile_x,
                tile_y,
                self.game_drawer.CELL_SIZE,
                self.game_drawer.CELL_SIZE,
            )

            # If there is a tile at that spot, draw the tile
            if tile is not None:
                pygame.draw.rect(
                    self.game_drawer.screen,
                    tile.BASE_COLOR,
                    rect,
                )
                pygame.draw.rect(
                    self.game_drawer.screen,
                    self.game_drawer.BORDER_COLOR,
                    rect,
                    1,
                )  # Draw border

                # Add the rect and tile to dictionary
                self.game_drawer.tile_rects[tile] = rect

                # Add text
                text_surface, rect = self.game_drawer.FONT.render(
                    str(tile), tile.TEXT_COLOR
                )
                text_x = tile_x + (self.game_drawer.CELL_SIZE - rect.width) / 2
                text_y = (
                    tile_y + (self.game_drawer.CELL_SIZE - rect.height) / 2
                )
                self.game_drawer.screen.blit(text_surface, (text_x, text_y))

            # If there is no tile, draw an empty spot
            else:
                pygame.draw.rect(
                    self.game_drawer.screen,
                    self.game_drawer.BACKGROUND_COLOR,
                    rect,
                )
                pygame.draw.rect(
                    self.game_drawer.screen,
                    self.game_drawer.BORDER_COLOR,
                    rect,
                    1,
                )  # Draw border

                # Add the empty spot to a dictionary
                self.game_drawer.empty_tiles_on_plank_index[i] = rect
