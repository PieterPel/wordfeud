from GameDrawer import GameDrawer

from Pile import Pile
from Board import Board
from Round import Round

import itertools
import pygame
import pygame.freetype  # Import the freetype module


class Game:
    def __init__(self, players: list):
        """
        Initialize a Game object.

        Args:
            players (list): A list of Player objects.
        """
        self.players = players
        self.players_iter = itertools.cycle(players)
        self.board = Board()
        self.pile = Pile()
        self.pile_iter = iter(self.pile)
        self.round_number = 0
        self.consecutive_passes = 0

    def begin_game(self):
        """
        Start the game.
        """
        self.add_players_to_game()
        self.distribute_tiles()
        self.new_round()

        print("Beginning game!")

        # Initialize Pygame
        pygame.init()

        drawer = GameDrawer(self)

        # Main PyGame loop
        running = True
        shown_player = self.players[0]  # TODO: change to correct player
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if an empty space on the board has been clicked on
                    for (
                        coordinates,
                        rect,
                    ) in drawer.coordinates_empty_cells.items():
                        if (
                            rect.collidepoint(mouse_pos)
                            and shown_player.selected_tile is not None
                            and (
                                coordinates
                                not in list(shown_player.current_move.values())
                            )
                        ):
                            shown_player.lay_tile_on_board(
                                shown_player.selected_tile, coordinates
                            )
                            print("Think there is an empty cell")

                    # Check if a tile has been clicked on
                    for tile, rect in drawer.tile_rects.items():
                        if rect.collidepoint(mouse_pos):
                            shown_player.select_tile(tile)

                    # Check if an empty plank space has been clicked on
                    for (
                        index,
                        rect,
                    ) in drawer.empty_tiles_on_pank_index.items():
                        if (
                            rect.collidepoint(mouse_pos)
                            and shown_player.selected_tile is not None
                        ):
                            shown_player.put_tile_on_plank(
                                shown_player.selected_tile, index
                            )

                    # Check if a button has been clicked on

                # Maybe return the elements that are drawn here, so the mouse can pick it up?
                drawer.reset_dicts()
                drawer.draw_board()
                drawer.draw_plank(shown_player)
                drawer.draw_current_move(shown_player)
                drawer.draw_aux(shown_player)
                # drawer.draw_buttons()

            # Update the display
            pygame.display.flip()

    def distribute_tiles(self):
        """
        Distribute tiles to each player's plank.
        """
        for player in self.players:
            while not player.plank.full:
                player.plank.add_tile(self.next_tile_from_pile)

    def add_players_to_game(self):
        """
        Add players to the game.
        """
        for player in self.players:
            player.enter_game(self)

    def new_round(self):
        """
        Start a new round.
        """
        self.round_number += 1
        self.round = Round(self, next(self.players_iter))

    def end_game(self):
        """
        End the game.
        """
        for player in self.players:
            player.exit_game()

    @property
    def next_tile_from_pile(self):
        """
        Get the next tile from the pile.

        Returns:
            Tile: The next tile from the pile.

        Raises:
            Exception: If the pile is empty.
        """
        if len(self.pile) == 0:
            raise Exception("The pile is empty!")

        return next(self.pile_iter)

    @property
    def empty_pile(self):
        """
        Check if the pile is empty.

        Returns:
            bool: True if the pile is empty, False otherwise.
        """
        return len(self.pile) == 0

    def add_tiles_to_pile(self, tiles: list):
        """
        Add tiles to the pile.

        Args:
            tiles (list): A list of Tile objects.
        """
        self.pile.add_tiles(tiles)
        self.pile_iter = iter(self.pile)
