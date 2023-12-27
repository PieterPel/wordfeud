from Tile import Tile


class Plank:
    LENGTH = 7

    def __init__(self):
        self._tile_list = [None] * self.LENGTH

    @property
    def full(self) -> bool:
        return not any([x is None for x in self._tile_list])

    @property
    def empty(self) -> bool:
        return all([x is None for x in self._tile_list])

    def add_tile(self, tile: Tile, index=None):
        if self.full:
            raise ValueError("This plank is full!")

        # Add tile to the provided index or the first element of _tile_list that is None
        if index is None or self[index] is not None:
            index = self._tile_list.index(None)

        self._tile_list[index] = tile

    def remove_tiles(self, tiles: list) -> None:
        # Update the tile list
        self._tile_list = [
            None if tile in tiles else self[i] for i, tile in enumerate(self)
        ]

    def get_tile_with_letter(self, letter: str) -> Tile:
        # Check for the letter on the tiles
        for tile in self:
            if tile.letter == letter:
                return tile

        # Return a blank if nto found and avalable
        if " " in self.letters:
            return self.get_tile_with_letter(" ")
        else:
            raise ValueError("This plank cannot provide that tile or a blank")

    @property
    def letters(self) -> list:
        letter_list = []
        for el in self:
            if el is not None:
                letter_list.append(el.letter)
        return letter_list

    @property
    def tile_list(self):
        return self._tile_list

    def __getitem__(self, index):
        return self._tile_list[index]

    def __repr__(self):
        return str(self._tile_list)
