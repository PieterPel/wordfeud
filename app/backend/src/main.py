from Player import Player
from Game import Game
import random


def main():
    random.seed(1914)

    # Create a Player instance
    player1 = Player("pete")
    player2 = Player("Mike")

    # Create a Game instance
    game = Game([player1, player2])

    game.begin_game()


if __name__ == "__main__":
    main()
