from Tile import Tile
import random
import copy


class Pile:
    INITIAL_AMOUNTS = {
        "A": 7,
        "B": 2,
        "C": 2,
        "D": 5,
        "E": 18,
        "F": 2,
        "G": 3,
        "H": 2,
        "I": 4,
        "J": 2,
        "K": 3,
        "L": 3,
        "M": 3,
        "N": 11,
        "O": 6,
        "P": 2,
        "Q": 1,
        "R": 5,
        "S": 5,
        "T": 5,
        "U": 3,
        "V": 2,
        "W": 2,
        "X": 1,
        "Y": 1,
        "Z": 2,
        " ": 2,
    }

    LETTER_POINTS = {
        "A": 1,
        "B": 4,
        "C": 5,
        "D": 2,
        "E": 1,
        "F": 4,
        "G": 3,
        "H": 4,
        "I": 2,
        "J": 4,
        "K": 3,
        "L": 3,
        "M": 3,
        "N": 1,
        "O": 1,
        "P": 4,
        "Q": 10,
        "R": 2,
        "S": 2,
        "T": 2,
        "U": 2,
        "V": 4,
        "W": 5,
        "X": 8,
        "Y": 8,
        "Z": 5,
        " ": 0,
    }

    def __init__(self):
        self.tile_list = self._set_up_list()

    def _set_up_list(self):
        tile_list = []

        for letter, amount in self.INITIAL_AMOUNTS.items():
            tile = Tile(letter, self.LETTER_POINTS[letter])
            tile_list.extend(copy.deepcopy(tile) for _ in range(amount))

        random.shuffle(tile_list)
        return tile_list

    def _add_tile(self, tile: Tile):
        self.tile_list.append(tile)

    def add_tiles(self, tiles: list):
        for tile in tiles:
            self._add_tile(tile)
        random.shuffle(self.tile_list)

    def __len__(self):
        return len(self.tile_list)

    def __iter__(self):
        return self

    def __next__(self):
        return self.tile_list.pop()
