class ScrollHandler:
    def __init__(self, game):
        self.game = game

    def handle_scroll(self, x, y):
        # If the player hasn't generated possible moves, do nothing
        if self.game.shown_player.possible_moves == []:
            return

        # Else update the players current move

        # Clear the current move
        self.game.shown_player.clear_current_move()
        new_index = self.game.shown_player.possible_moves_index + y
        new_index = max(0, new_index)
        new_index = min(
            len(self.game.shown_player.possible_moves) - 1, new_index
        )
        self.game.shown_player.possible_moves_index = new_index
        self.game.shown_player.lay_move_on_board(
            self.game.shown_player.possible_moves[new_index]
        )
