from collections import UserDict


class Move(UserDict):
    WIDTH = 15
    HEIGHT = 15

    def get_direction(self) -> str:
        coordinates = list(self.values())
        num_different_x = len(set(x for x, _ in coordinates))
        num_different_y = len(set(y for _, y in coordinates))
        direction = None

        # Check for verticality
        if num_different_x == 1 and num_different_y > 1:
            direction = "Vertical"
        elif num_different_y == 1 and num_different_x > 1:
            direction = "Horizontal"
        return direction

    def get_turned_move(self):
        # transpose, then flip columns
        turned_move = Move(
            {tile: (y, self.HEIGHT - 1 - x) for tile, (x, y) in self.items()}
        )

        return turned_move

    def __repr__(self):
        string = ""

        for tile in list(self.keys()):
            string += str(tile)

        return string
