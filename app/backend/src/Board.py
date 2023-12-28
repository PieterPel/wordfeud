from Cell import Cell
from LegalityChecker import LegalityChecker
import os
import copy

BINGO_BONUS = 40


def get_points_of_word(points, muls):
    # Letters dont make words
    length = len(points)
    if length < 2:
        return 0
    else:
        word_points = 0
        total_word_mul = 1
        for point, mul in zip(points, muls):
            match mul:
                case "":
                    word_points += point
                case "2L":
                    word_points += 2 * point
                case "3L":
                    word_points += 3 * point
                case "2W":
                    word_points += point
                    total_word_mul *= 2
                case "3W":
                    word_points += point
                    total_word_mul *= 3

        if length == 7:
            points = total_word_mul * word_points + BINGO_BONUS
        else:
            points = total_word_mul * word_points

        return points


def get_word_set():
    word_set = set()
    with open(
        f"{os.getcwd()}/wordlists/wordlist-edited.txt", "r"
    ) as word_list:
        for word in word_list:
            word_set.add(
                word[:-1].upper()
            )  # Remove "\n" and put in upper case
    return word_set


class Board:
    """
    Represents the game board.
    """

    HEIGHT = 15
    LENGTH = 15
    MIDDLE = (7, 7)
    WORD_SET = get_word_set()

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

    def get_points_of_move(self, move: dict) -> int:
        """
        Get the new words created by the move.

        Args:
            move (dict): The move to check.

        Returns:
            set: The set of new words.
        """
        reverse_move_dict = {value: key for key, value in move.items()}
        total_points = 0
        scanned_vertically = False
        scanned_horizontally = False
        move_direction = move.get_direction()

        for tile, coordinates in move.items():
            x, y = coordinates

            def scan_direction(dx, dy):
                # Initialize
                scanner_x, scanner_y = x + dx, y + dy
                letters = ""
                multipliers = []
                points = []

                # While there is a tile, store the letter (points and multiplier)
                while self[scanner_x, scanner_y].filled or (
                    scanner_x,
                    scanner_y,
                ) in list(move.values()):
                    # If the tile is on the board
                    if self[scanner_x, scanner_y].filled:
                        scanned_tile = self[scanner_x, scanner_y].tile

                    # If the tile is in the move
                    else:
                        scanned_tile = reverse_move_dict[
                            (scanner_x, scanner_y)
                        ]

                    # Update letters, points and multipliers
                    letters += scanned_tile.letter
                    points.append(scanned_tile.points)
                    multipliers.append(self[scanner_x, scanner_y].multiplier)

                    scanner_x += dx
                    scanner_y += dy

                return {
                    "letters": letters,
                    "points": points,
                    "multipliers": multipliers,
                }

            # Scan vertically
            if not (scanned_vertically and move_direction == "Vertical"):
                above = scan_direction(0, 1)
                below = scan_direction(0, -1)

                # Update points of vertical scan
                points_vertical = (
                    above["points"] + [tile.points] + below["points"]
                )
                muls_vertical = (
                    above["multipliers"]
                    + [self[x, y].multiplier]
                    + below["multipliers"]
                )

                total_points += get_points_of_word(
                    points_vertical, muls_vertical
                )
                scanned_vertically = True

            # Scan horizontally
            if not (scanned_horizontally and move_direction == "Horizontal"):
                left = scan_direction(-1, 0)
                right = scan_direction(1, 0)

                # Update points of horizontal scan
                points_horizontal = (
                    left["points"] + [tile.points] + right["points"]
                )

                muls_horizontal = (
                    left["multipliers"]
                    + [self[x, y].multiplier]
                    + right["multipliers"]
                )

                total_points += get_points_of_word(
                    points_horizontal, muls_horizontal
                )

                scanned_horizontally = True

        return total_points

    def __getitem__(self, coordinates: tuple):
        x, y = coordinates

        # Return an empty cell if the coordinate arent on the board
        if x < 0 or y < 0 or x > self.LENGTH - 1 or y > self.HEIGHT:
            return Cell(-1, -1, "")
        # Else return the cell at the grid
        else:
            return self.grid[x][y]

    def get_turned_board(self):
        copy_board = copy.deepcopy(self)

        # Transpose and reverse the grid
        copy_board.grid = {
            self.LENGTH
            - 1
            - x: {
                self.HEIGHT - 1 - y: copy_board.grid[y][x]
                for y in range(copy_board.HEIGHT)
            }
            for x in range(copy_board.LENGTH)
        }

        # Update filled_coordinates with the rotated coordinates
        copy_board.filled_coordinates = [
            (self.LENGTH - 1 - y, self.HEIGHT - 1 - x)
            for x, y in copy_board.filled_coordinates
        ]

        return copy_board
