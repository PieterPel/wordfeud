class Cell:
    MIDDLE = 7
    TEXT_COLOR = (255, 255, 255)
    MULT_COLOR_DICT = {
        "": (55, 51, 64),
        "2W": (201, 117, 32),
        "3W": (227, 7, 14),
        "2L": (24, 125, 56),
        "3L": (0, 51, 204),
    }

    def __init__(self, x, y, multiplier):
        self._x = x
        self._y = y
        self.multiplier = multiplier
        self._tile = None
        self.locked = False

    def __repr__(self):
        return str(self.tile)

    @property
    def base_color(self):
        if self.x == self.y == self.MIDDLE:
            return (139, 23, 145)

        return self.MULT_COLOR_DICT[self.multiplier]

    @property
    def filled(self):
        return self._tile is not None

    @property
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, new_tile):
        self._multiplier = ""
        self._tile = new_tile
        self.locked = True

    # Ensure that x, y and multiplier are "read only"
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
