class Round:
    def __init__(self, game, player_laying):
        self.game = game
        self.player_laying = player_laying

        self.begin_round()

    def begin_round(self):
        self.player_laying.begin_turn()
