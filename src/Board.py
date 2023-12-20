from Cell import Cell


def checkConsecutive(li):
    """
    Check if a list contains consecutive numbers.

    Args:
        li (list): The list to check.

    Returns:
        bool: True if the list contains consecutive numbers, False otherwise.
    """
    return sorted(li) == list(range(min(li), max(li) + 1))


class Board:
    """
    Represents the game board.
    """

    word_set = set()
    HEIGHT = 15
    LENGTH = 15

    LOC_MULTIPLIERS = {(0, 0): "3L", (1, 1): "2W"}

    def __init__(self):
        """
        Initialize a new instance of the Board class.
        """
        self.grid = self._set_up_grid()
        self.filled_coordinates = []

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
        coordinates = list(move.values())

        if not self._correct_coordinates(coordinates):
            return False

        new_words = self.get_new_words(move)
        if new_words.issubset(self.word_set):
            return True
        else:
            print(f"{new_words - self.word_set} is/aren't allowed")
            return False

    def _correct_coordinates(self, coordinates: list) -> bool:
        """
        Check if the given coordinates can make up a correct move.

        Args:
            coordinates (list): The coordinates to check.

        Returns:
            bool: True if the coordinates are correct, False otherwise.
        """
        coordinate_check = [
            True if x > self.LENGTH or y > self.HEIGHT else False
            for x, y in coordinates
        ]
        if any(coordinate_check):
            print("At least one of these coordinates is too large")
            return False

        if not len(set(coordinates)) == len(coordinates):
            print("There are duplicate coordinates")
            return False

        filled_check = [
            True if self[x][y].filled else False for x, y in coordinates
        ]
        if any(filled_check):
            print("Illegal move, one of the cells is already filled")
            return False

        all_x = [x for x, _ in coordinates]
        all_y = [y for _, y in coordinates]
        if not (
            len(set(all_x)) == 1
            and checkConsecutive(all_y)
            or len(set(all_y)) != 1
            and checkConsecutive(all_x)
        ):
            print("The tiles aren't in a straight line")
            return False

        if not any(
            coord in self.required_coordinates() for coord in coordinates
        ):
            return False

        return True

    def required_coordinates(self) -> set:
        """
        Get the coordinates of the filled cells and their neighbors.

        Returns:
            set: The set of required coordinates.
        """
        filled_neighbors = set()
        for x, y in self.filled_coordinates:
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            filled_neighbors.update(neighbors)
        return filled_neighbors

    def lay_word_on_board(self, move: dict) -> None:
        """
        Lay the word on the board.

        Args:
            move (dict): The move to lay on the board.
        """
        self.filled_coordinates.extend(list(move.keys()))

        for tile, coordinates in move.items():
            x, y = coordinates
            self[x][y].tile = tile

    def get_new_words(self, move: dict) -> set:
        """
        Get the new words created by the move.

        Args:
            move (dict): The move to check.

        Returns:
            set: The set of new words.
        """
        new_words = set()

        for tile, coordinates in move.items():
            x, y = coordinates

            def scan_direction(dx, dy):
                scanner_x, scanner_y = x + dx, y + dy
                letters = ""
                while self[scanner_x][scanner_y].filled:
                    letters += self[scanner_x][scanner_y].letter
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

        return new_words

    def __getitem__(self, coordinates: tuple):
        x, y = coordinates
        return self.grid[x][y]
