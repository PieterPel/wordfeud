from Player import Player
from Tile import Tile
from Game import Game


def main():
    # Create a Player instance
    player = Player("pete")

    # Create a Game instance
    game = Game([player])
    board = game.board
    tile = Tile("B", 4)
    board[0, 1].tile = tile

    game.begin_game()


if __name__ == "__main__":
    print("test")
    main()
