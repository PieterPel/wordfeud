from Cell import Cell
from LegalityChecker import LegalityChecker


class Board:
    """
    Represents the game board.
    """

    word_set = set()
    HEIGHT = 15
    LENGTH = 15
    MIDDLE = (7, 7)

    LOC_MULTIPLIERS = {
        # Bottom left quadrant
        (0, 0): "3L",
        (1, 1): "2L",
        (2, 2): "2W",
        (3, 3): "3L",
        (4, 4): "2W",
        (5, 5): "3L",
        (0, 4): "3W",
        (1, 5): "3L",
        (2, 6): "2L",
        (4, 6): "2L",
        (4, 0): "3W",
        (5, 1): "3L",
        (6, 2): "2L",
        (6, 4): "2L",
        # Top left quadrant
        (0, 14): "3L",
        (1, 13): "2L",
        (2, 12): "2W",
        (3, 11): "3L",
        (4, 10): "2W",
        (5, 9): "3L",
        (0, 10): "3W",
        (1, 9): "3L",
        (2, 8): "2L",
        (4, 8): "2L",
        (4, 14): "3W",
        (5, 13): "3L",
        (6, 12): "2L",
        (6, 10): "2L",
        # Bottom right quadrant
        (14, 0): "3L",
        (13, 1): "2L",
        (12, 2): "2W",
        (11, 3): "3L",
        (10, 4): "2W",
        (9, 5): "3L",
        (14, 4): "3W",
        (13, 5): "3L",
        (12, 6): "2L",
        (12, 8): "2L",
        (10, 0): "3W",
        (9, 1): "3L",
        (8, 2): "2L",
        (8, 4): "2L",
        # Top right quadrant
        (14, 14): "3L",
        (13, 13): "2L",
        (12, 12): "2W",
        (11, 11): "3L",
        (10, 10): "2W",
        (9, 9): "3L",
        (14, 10): "3W",
        (13, 9): "3L",
        (12, 8): "2L",
        (10, 8): "2L",
        (10, 14): "3W",
        (9, 13): "3L",
        (8, 12): "2L",
        (8, 10): "2L",
        # Cross
        (7, 0): "2L",
        (7, 3): "2W",
        (0, 7): "2L",
        (3, 7): "2W",
        (7, 14): "2L",
        (7, 11): "2W",
        (14, 7): "2L",
        (11, 7): "2W",
    }

    def __init__(self):
        """
        Initialize a new instance of the Board class.
        """
        self.grid = self._set_up_grid()
        self.filled_coordinates = []
        self.legality_checker = LegalityChecker(self)

    def _set_up_grid(self) -> dict:
        """
        Set up the grid for the board.

        Returns:
            dict: The grid representing the board.
        """
        grid = {
            x: {
                y: Cell(x, y, self.LOC_MULTIPLIERS.get((x, y), ""))
                for y in range(self.HEIGHT)
            }
            for x in range(self.LENGTH)
        }
        return grid

    def legal_move(self, move: dict) -> bool:
        """
        Check if a move is legal.

        Args:
            move (dict): The move to check.

        Returns:
            bool: True if the move is legal, False otherwise.
        """

        return self.legality_checker.legal_move(move)

    def lay_word_on_board(self, move: dict) -> None:
        """
        Lay the word on the board.

        Args:
            move (dict): The move to lay on the board.
        """
        self.filled_coordinates.extend(list(move.values()))

        for tile, coordinates in move.items():
            x, y = coordinates
            self[x, y].tile = tile
            self[x, y].multiplier = ""

    # TODO: properly implement
    def get_points_of_move(self, move: dict):
        points = 0

        for tile, coordinates in move.items():
            x, y = coordinates

            def scan_direction(dx, dy):
                scanner_x, scanner_y = x + dx, y + dy
                letters = ""
                while self.board[scanner_x, scanner_y].filled:
                    letters += self.board[scanner_x, scanner_y].letter
                    scanner_x += dx
                    scanner_y += dy
                return letters

            letters_above = scan_direction(0, 1)
            letters_below = scan_direction(0, -1)
            letters_left = scan_direction(-1, 0)
            letters_right = scan_direction(1, 0)

            new_words.update(
                word
                for word in [
                    f"{letters_above[::-1]}{tile.letter}{letters_below}",
                    f"{letters_left[::-1]}{tile.letter}{letters_right}",
                ]
                if len(word) > 1
            )

        return points

    def __getitem__(self, coordinates: tuple):
        x, y = coordinates
        return self.grid[x][y]
