class LegalityChecker:
    def __init__(self, board):
        self.board = board
        self.WORD_SET = self.board.WORD_SET

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
        print(f"Formed words: {new_words}")
        if new_words.issubset(self.WORD_SET) and len(new_words) > 0:
            return True
        else:
            print(f"{new_words - self.WORD_SET} is/aren't allowed")
            return False

    def _correct_coordinates(self, coordinates: list) -> bool:
        """
        Check if the given coordinates can make up a correct move.

        Args:
            coordinates (list): The coordinates to check.

        Returns:
            bool: True if the coordinates are correct, False otherwise.
        """
        # Check if the coordinates are in the right range
        coordinate_check = [
            True if x > self.board.LENGTH or y > self.board.HEIGHT else False
            for x, y in coordinates
        ]
        if any(coordinate_check):
            print("At least one of these coordinates is too large")
            return False

        # Check for duplicate coordinates
        if not len(set(coordinates)) == len(coordinates):
            print("There are duplicate coordinates")
            return False

        # Check for already filled coordinates
        filled_check = [
            True if self.board[x, y].filled else False for x, y in coordinates
        ]
        if any(filled_check):
            print("Illegal move, one of the cells is already filled")
            return False

        # Check for the move forming a connecting straight line
        all_x = [x for x, _ in coordinates]
        all_y = [y for _, y in coordinates]
        filled_on_board = self.board.filled_coordinates

        # First check if all x's are the same
        if len(set(all_x)) == 1:
            # Then we should have no gaps in y
            missing_y = find_missing(sorted(all_y))
            for y in missing_y:
                if not (all_x[0], y) in filled_on_board:
                    print("There is a gap")
                    return False

        # Then check if all y's are the same
        elif len(set(all_y)) == 1:
            # Then we should have no gaps in x
            missing_x = find_missing(sorted(all_x))
            for x in missing_x:
                if not (x, all_y[0]) in filled_on_board:
                    print("There is a gap")
                    return False
        else:
            print("The tiles aren't in a straight line")
            return False

        # Check if the word touches an existing tile on the board
        if not any(
            coord in self.required_coordinates() for coord in coordinates
        ):
            print("This move doesnt touch an existing tile")
            return False

        return True

    def required_coordinates(self) -> set:
        """
        Get the coordinates of the filled cells and their neighbors.

        Returns:
            set: The set of required coordinates.
        """
        filled_neighbors = set([self.board.MIDDLE])
        for x, y in self.board.filled_coordinates:
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            filled_neighbors.update(neighbors)
        return filled_neighbors

    def get_new_words(self, move: dict) -> set:
        """
        Get the new words created by the move.

        Args:
            move (dict): The move to check.

        Returns:
            set: The set of new words.
        """
        new_words = set()
        reverse_move_dict = {value: key for key, value in move.items()}

        for tile, coordinates in move.items():
            x, y = coordinates

            def scan_direction(dx, dy):
                # Initialize
                scanner_x, scanner_y = x + dx, y + dy
                letters = ""

                # While there is a tile, store the letter
                while self.board[scanner_x, scanner_y].filled or (
                    scanner_x,
                    scanner_y,
                ) in list(move.values()):
                    # If the tile is on the board
                    if self.board[scanner_x, scanner_y].filled:
                        letters += self.board[scanner_x, scanner_y].tile.letter

                    # If the tile is in the move
                    else:
                        letters += reverse_move_dict[
                            (scanner_x, scanner_y)
                        ].letter
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


def checkConsecutive(li):
    """
    Check if a list contains consecutive numbers.

    Args:
        li (list): The list to check.

    Returns:
        bool: True if the list contains consecutive numbers, False otherwise.
    """
    return sorted(li) == list(range(min(li), max(li) + 1))


def find_missing(lst):
    """
    Source: https://www.geeksforgeeks.org/python-find-missing-numbers-in-a-sorted-list-range/
    """
    return [
        i for x, y in zip(lst, lst[1:]) for i in range(x + 1, y) if y - x > 1
    ]
