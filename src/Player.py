from Plank import Plank
from Game import Game
from Tile import Tile


# Very hacky but it works
def only_on_turn(func):
    def wrap(self, *args, **kwargs):
        """
        Decorator that checks if it is the player's turn before executing the function.
        """
        if self.laying:
            func(self, *args, **kwargs)
        else:
            raise Exception(f"It is not {self.name}'s turn!")

    return wrap


class Player:
    def __init__(self, name: str):
        """
        Initializes a Player object with the given name.
        """
        self.name = name
        self._plank = Plank()
        self.score = 0
        self._game = None
        self.laying = False

        self.selected_tile = None
        self.current_move = {}

    @property
    def in_game(self):
        """
        Returns True if the player is currently in a game, False otherwise.
        """
        return self.game is not None

    @property
    def plank(self):
        """
        Returns the player's plank.
        """
        return self._plank

    @property
    def game(self):
        """
        Returns the game the player is currently in.
        """
        return self._game

    def enter_game(self, game: Game):
        """
        Enters the player into the given game.
        """
        self._game = game

    def exit_game(self):
        """
        Exits the current game and resets player's attributes.
        """
        self.game = None
        self.plank = Plank()
        self.score = 0

    # TODO: implement
    def begin_turn(self):
        """
        Begins the player's turn.
        """
        self.laying = True

        # Rough workflow:

        # Option 1) Skip
        # Option 2) Swap
        # Option 3) Select a tile

        # Put on board or on plank

        # If put on board, add to the current_move dictionary

    def select_tile(self, tile: Tile):
        """
        Selects a tile for the current move.
        """

        # Do something with currently selected tile, swap?
        print(f"Trying to select {tile}")

        # If tile part of current move, remove it
        if tile in self.current_move.keys():
            del self.current_move[tile]

        # If tile on plank, remove it
        if tile in self.plank:
            self.plank.remove_tiles([tile])

            if self.selected_tile is not None:
                self.plank.add_tile(self.selected_tile)

        print(f"selecting: {str(tile)}")
        self.selected_tile = tile

    def lay_tile_on_board(self, tile: Tile, coordinates: tuple):
        """
        Places a tile on the game board at the specified coordinates.
        """
        x, y = coordinates

        print(f"Trying to lay {tile} at {coordinates}")

        # Check whether cell filled at those coordinates
        if self.game.board[(x, y)].filled:
            raise ValueError(
                "This cell is already filled"
            )  # TODO handle error better, just do nothing maybe?
        # Check whether already tile on board as part of current move
        if coordinates in self.current_move.values():
            # Get the key for which the condition is true
            current_tile = next(
                key
                for key, value in self.current_move.items()
                if value == coordinates
            )
            del self.current_move[current_tile]
            self.selected_tile = current_tile

        else:
            self.current_move[tile] = coordinates
            self.selected_tile = None

        print(f"Current move: {self.current_move}")

    def put_tile_on_plank(self, tile: Tile, index=None):
        self.plank.add_tile(tile, index)
        self.selected_tile = None

    def clear_current_move(self):
        # Add tiles to plank
        for tile in list(self.current_move.keys()):
            self.plank.add_tile(tile)

        # Empty current move
        self.current_move = {}

    @only_on_turn
    def play_current_move(self):
        """
        Lays a word on the game board as part of the player's move.
        """
        if self.game.board.legal_move(self.current_move):
            self.game.board.lay_word_on_board(self.current_move)
            self.game.consecutive_passes = 0
            self.current_move = {}

            # TODO: Add score to total score

            self.end_turn()
        else:
            print("This move is not legal, try something else")
            self.begin_turn()

    @only_on_turn
    def swap(self, tiles):
        """
        Swaps the specified tiles from the player's plank with new tiles from the game pile.
        """

        # Not allowed if fewer than the plank length in the pile
        if len(self.game.pile) <= self.plank.LENGTH:
            print("Not enough tiles in the pile to swap, try something else")
            self.begin_turn()

        # Remove the tiles from the plank and add them to the pile
        self.plank.remove_tiles(tiles)
        self.game.add_tiles_to_pile(tiles)

        self.end_turn()

    @only_on_turn
    def skip(self):
        """
        Skips the player's turn.
        """
        self.game.consecutive_passes += 1
        self.end_turn()

    @only_on_turn
    def end_turn(self):
        """
        Ends the player's turn.
        """
        self.laying = False

        # Draw new tiles
        self.draw_tiles()

        # End the game or begin a new round
        if len(self.plank) == 0 or (
            self.game.consecutive_passes > 2 * len(self.game.players)
        ):
            self.game.end_game()
        else:
            self.game.new_round()

    def draw_tiles(self):
        while not self.plank.full and not self.game.empty_pile:
            drawn_tile = self.game.next_tile_from_pile
            self.plank.add_tile(drawn_tile)
