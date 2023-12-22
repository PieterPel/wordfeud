import pygame


class OtherDrawer:
    def __init__(self, game_drawer):
        self.game_drawer = game_drawer

    # TODO: score(s),  number of tiles left
    def draw(self, player):
        # Draw currently selected tile
        if player.selected_tile is not None:
            # Get the current mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Create a rectangle for the tile at the mouse position
            rectt = pygame.Rect(
                mouse_x,
                mouse_y,
                self.game_drawer.CELL_SIZE,
                self.game_drawer.CELL_SIZE,
            )

            # Draw the rectangle
            pygame.draw.rect(
                self.game_drawer.screen,
                player.selected_tile.BASE_COLOR,
                rectt,
            )

            # Draw the tile number
            text_surface, _ = self.game_drawer.FONT.render(
                str(player.selected_tile), player.selected_tile.TEXT_COLOR
            )
            text_x = mouse_x + (self.game_drawer.CELL_SIZE - _.width) / 2
            text_y = mouse_y + (self.game_drawer.CELL_SIZE - _.height) / 2
            self.game_drawer.screen.blit(text_surface, (text_x, text_y))

        # Add round number
        round_text = "Round: " + str(self.game_drawer.game.round_number)
        round_text_surface, round_rect = self.game_drawer.FONT.render(
            round_text, self.game_drawer.TEXT_COLOR
        )
        round_text_x = (
            self.game_drawer.WIDTH
            - round_rect.width
            - self.game_drawer.BORDER_WIDTH
        )
        round_text_y = (
            self.game_drawer.HEIGHT
            + self.game_drawer.CELL_SIZE
            + self.game_drawer.BORDER_WIDTH
        )
        self.game_drawer.screen.blit(
            round_text_surface, (round_text_x, round_text_y)
        )

        # Add player's score
        score_text = "Score: " + str(player.score)
        score_text_surface, score_rect = self.game_drawer.FONT.render(
            score_text, self.game_drawer.TEXT_COLOR
        )
        score_text_x = (
            self.game_drawer.WIDTH
            - score_rect.width
            - self.game_drawer.BORDER_WIDTH
        )
        score_text_y = (
            round_text_y - score_rect.height - self.game_drawer.BORDER_WIDTH
        )
        self.game_drawer.screen.blit(
            score_text_surface, (score_text_x, score_text_y)
        )
