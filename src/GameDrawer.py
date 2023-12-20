import pygame
import pygame.freetype


class GameDrawer:
    # Set up some constants
    CELL_SIZE = 40  # You can change this to whatever you like
    GAP_SIZE = 0  # TODO Make the tiles have a gap between them
    BORDER_WIDTH = 5
    BORDER_COLOR = (0, 0, 0)  # RGB color for black
    BACKGROUND_COLOR = (20, 20, 20)
    TEXT_COLOR = (255, 255, 255)
    HIGHLIGHT_COLOR = (150, 150, 150)

    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.WIDTH = self.board.LENGTH * self.CELL_SIZE
        self.HEIGHT = self.board.HEIGHT * self.CELL_SIZE
        self.FONT = pygame.freetype.SysFont("Calibri", 28)
        self.tile_rects = {}
        self.empty_tiles_on_pank_index = {}
        self.coordinates_empty_cells = {}

        self.screen = pygame.display.set_mode(
            (
                self.WIDTH + 2 * self.BORDER_WIDTH,
                self.HEIGHT + 3 * self.CELL_SIZE + 2 * self.BORDER_WIDTH,
            )
        )

    def reset_dicts(self):
        self.tile_rects = {}
        self.empty_tiles_on_pank_index = {}
        self.coordinates_empty_cells = {}

    def draw_board(self):
        # Fill the background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw the border
        pygame.draw.rect(
            self.screen,
            self.BORDER_COLOR,
            pygame.Rect(
                0,
                0,
                self.WIDTH + 2 * self.BORDER_WIDTH,
                self.HEIGHT + 3 * self.CELL_SIZE + 2 * self.BORDER_WIDTH,
            ),
            self.BORDER_WIDTH,
        )

        # Draw the board
        for y in range(self.board.HEIGHT):
            for x in range(self.board.LENGTH):
                cell = self.board[x, y]

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
                    self.BORDER_WIDTH + x * self.CELL_SIZE,
                    self.BORDER_WIDTH
                    + (self.board.HEIGHT - 1 - y) * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                )

                pygame.draw.rect(self.screen, base_color, rect)

                # Draw border
                pygame.draw.rect(
                    self.screen,
                    self.BORDER_COLOR,
                    rect,
                    1,
                )

                # Add empty cell rect to list
                if not cell.tile:
                    self.coordinates_empty_cells[(x, y)] = rect

                # Add text if necessary
                if not text == "":
                    text_surface, rect = self.FONT.render(text, text_color)
                    text_x = (
                        self.BORDER_WIDTH
                        + x * self.CELL_SIZE
                        + (self.CELL_SIZE - rect.width) / 2
                    )
                    text_y = (
                        self.BORDER_WIDTH
                        + (self.board.HEIGHT - 1 - y) * self.CELL_SIZE
                        + (self.CELL_SIZE - rect.height) / 2
                    )
                    self.screen.blit(text_surface, (text_x, text_y))

    def draw_plank(self, player):
        # Draw the plank
        for i, tile in enumerate(player.plank):
            tile_x = self.BORDER_WIDTH + i * self.CELL_SIZE
            tile_y = self.HEIGHT + 2 * self.BORDER_WIDTH
            rect = pygame.Rect(tile_x, tile_y, self.CELL_SIZE, self.CELL_SIZE)

            # If there is a tile at that spot, draw the tile
            if tile is not None:
                pygame.draw.rect(
                    self.screen,
                    tile.BASE_COLOR,
                    rect,
                )
                pygame.draw.rect(
                    self.screen,
                    self.BORDER_COLOR,
                    rect,
                    1,
                )  # Draw border

                # Add the rect and tile to dictionary
                self.tile_rects[tile] = rect

                # Add text
                text_surface, rect = self.FONT.render(
                    str(tile), tile.TEXT_COLOR
                )
                text_x = tile_x + (self.CELL_SIZE - rect.width) / 2
                text_y = tile_y + (self.CELL_SIZE - rect.height) / 2
                self.screen.blit(text_surface, (text_x, text_y))

            # If there is no tile, draw an empty spot
            else:
                pygame.draw.rect(
                    self.screen,
                    self.BACKGROUND_COLOR,
                    rect,
                )
                pygame.draw.rect(
                    self.screen,
                    self.BORDER_COLOR,
                    rect,
                    1,
                )  # Draw border

                # Add the empty spot to a dictionary
                self.empty_tiles_on_pank_index[i] = rect

    def draw_current_move(self, player):
        # Assuming player.current_move is the dictionary representing the move
        for tile, (x, y) in player.current_move.items():
            # Create a rectangle for the tile
            rect = pygame.Rect(
                self.BORDER_WIDTH + x * self.CELL_SIZE,
                self.BORDER_WIDTH
                + (self.board.HEIGHT - 1 - y) * self.CELL_SIZE,
                self.CELL_SIZE - self.GAP_SIZE,
                self.CELL_SIZE - self.GAP_SIZE,
            )

            # # Draw the rectangle with a different color to highlight it
            # pygame.draw.rect(
            #     self.screen,
            #     self.HIGHLIGHT_COLOR,  # Define this color in your __init__ method
            #     rect,
            #     3,  # Increase border width to make it more noticeable
            # )

            pygame.draw.rect(
                self.screen,
                tile.BASE_COLOR,
                rect,
            )

            # Add drawn tile to dictionary so it can be clicked
            self.tile_rects[tile] = rect

            # Add text if necessary
            text_surface, rect = self.FONT.render(str(tile), tile.TEXT_COLOR)
            text_x = (
                self.BORDER_WIDTH
                + x * self.CELL_SIZE
                + (self.CELL_SIZE - rect.width) / 2
            )
            text_y = (
                self.BORDER_WIDTH
                + (self.board.HEIGHT - 1 - y) * self.CELL_SIZE
                + (self.CELL_SIZE - rect.height) / 2
            )
            self.screen.blit(text_surface, (text_x, text_y))

    # TODO: score(s),  number of tiles left
    def draw_aux(self, player):
        # Draw currently selected tile
        if player.selected_tile is not None:
            # Get the current mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Create a rectangle for the tile at the mouse position
            rectt = pygame.Rect(
                mouse_x, mouse_y, self.CELL_SIZE, self.CELL_SIZE
            )

            # Draw the rectangle
            pygame.draw.rect(
                self.screen,
                player.selected_tile.BASE_COLOR,
                rectt,
            )

            # Draw the tile number
            text_surface, _ = self.FONT.render(
                str(player.selected_tile), player.selected_tile.TEXT_COLOR
            )
            text_x = mouse_x + (self.CELL_SIZE - _.width) / 2
            text_y = mouse_y + (self.CELL_SIZE - _.height) / 2
            self.screen.blit(text_surface, (text_x, text_y))

        # Add round number
        round_text = "Round: " + str(self.game.round_number)
        round_text_surface, round_rect = self.FONT.render(
            round_text, self.TEXT_COLOR
        )
        round_text_x = self.WIDTH - round_rect.width - self.BORDER_WIDTH
        round_text_y = self.HEIGHT + self.CELL_SIZE + self.BORDER_WIDTH
        self.screen.blit(round_text_surface, (round_text_x, round_text_y))

        # Add player's score
        score_text = "Score: " + str(player.score)
        score_text_surface, score_rect = self.FONT.render(
            score_text, self.TEXT_COLOR
        )
        score_text_x = self.WIDTH - score_rect.width - self.BORDER_WIDTH
        score_text_y = round_text_y - score_rect.height - self.BORDER_WIDTH
        self.screen.blit(score_text_surface, (score_text_x, score_text_y))

    def draw_buttons(self):
        # Draw "Clear Board" button
        clear_button_rect = pygame.Rect(50, self.HEIGHT - 50, 100, 50)
        pygame.draw.rect(
            self.screen, (255, 0, 0), clear_button_rect
        )  # Red button
        clear_button_text = self.FONT.render(
            "Clear Board", True, (255, 255, 255)
        )  # White text
        self.screen.blit(clear_button_text, (60, self.HEIGHT - 40))

        # Draw "Play Move" button
        play_button_rect = pygame.Rect(200, self.HEIGHT - 50, 100, 50)
        pygame.draw.rect(
            self.screen, (0, 255, 0), play_button_rect
        )  # Green button
        play_button_text = self.FONT.render(
            "Play Move", True, (255, 255, 255)
        )  # White text
        self.screen.blit(play_button_text, (210, self.HEIGHT - 40))
