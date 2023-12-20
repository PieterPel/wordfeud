from Tile import Tile


class Plank:
    LENGTH = 7

    def __init__(self):
        self._tile_list = [None] * self.LENGTH

    @property
    def full(self) -> bool:
        return not any([x is None for x in self._tile_list])

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

    def __getitem__(self, index):
        return self._tile_list[index]

    def __repr__(self):
        return str(self._tile_list)