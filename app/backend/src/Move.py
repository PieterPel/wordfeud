from collections import UserDict


class Move(UserDict):
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
