from Pile import Pile
from Board import Board
from Round import Round
from Engine import Engine

import sys
import os
from os.path import realpath, join, dirname

import itertools
import pygame
import pygame.freetype  # Import the freetype module


# TODO: change to package when finished so this is 100x times better
print(os.getcwd())
sys.path.append(f"{os.getcwd()}/app/frontend/src")
from GameDrawer import GameDrawer
from ClickHandler import ClickHandler


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
        self.engine = Engine(self.board)
        self.pile = Pile()
        self.pile_iter = iter(self.pile)
        self.round_number = 0
        self.consecutive_passes = 0
        self.shown_player = self.players[0]

    def begin_game(self):
        """
        Start the game.
        """
        self.add_players_to_game()
        self.distribute_tiles()
        self.new_round()
        turned = False

        print("Beginning game!")

        # Initialize Pygame
        pygame.init()

        drawer = GameDrawer(self)
        click_handler = ClickHandler(self, drawer)

        # Main PyGame loop
        running = True  # TODO: change to correct player
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    click_handler.handle_click(mouse_pos)

                drawer.draw_all(self.shown_player)

            # Update the display
            pygame.display.flip()
            if self.round_number == 3 and not turned:
                self.board = self.board.get_turned_board()
                print(self.board.filled_coordinates)
                drawer = GameDrawer(self)
                click_handler = ClickHandler(self, drawer)
                turned = True

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
        next_player = next(self.players_iter)
        self.shown_player = next_player
        self.round = Round(self, next_player)

        # Test the engine
        moves = self.engine.find_possible_moves(self.shown_player.plank)
        print(moves[:20])
        print(len(moves))

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
