class ClickHandler:
    def __init__(self, game, drawer):
        self.game = game
        self.drawer = drawer

    def handle_click(self, mouse_pos):
        """
        Handle a click on the screen.
        """
        self.handle_empty_board_space(mouse_pos)
        self.handle_tile(mouse_pos)
        self.handle_empty_plank_space(mouse_pos)
        self.handle_button(mouse_pos)

    def handle_empty_board_space(self, mouse_pos):
        # Check if an empty space on the board has been clicked on
        for (
            coordinates,
            rect,
        ) in self.drawer.coordinates_empty_cells.items():
            if (
                rect.collidepoint(mouse_pos)
                and self.game.shown_player.selected_tile is not None
                and (
                    coordinates
                    not in list(self.game.shown_player.current_move.values())
                )
            ):
                self.game.shown_player.lay_tile_on_board(
                    self.game.shown_player.selected_tile, coordinates
                )

    def handle_tile(self, mouse_pos):
        # Check if a tile has been clicked on
        for tile, rect in self.drawer.tile_rects.items():
            if rect.collidepoint(mouse_pos):
                # Check if the tile is part of the current move
                print(f"You clicked {tile}")
                if (
                    tile in self.game.shown_player.current_move
                    and self.game.shown_player.selected_tile is not None
                ):
                    coordinates = self.game.shown_player.current_move[tile]
                    self.game.shown_player.lay_tile_on_board(
                        self.game.shown_player.selected_tile,
                        coordinates,
                    )

                self.game.shown_player.select_tile(tile)

    def handle_empty_plank_space(self, mouse_pos):
        # Check if an empty plank space has been clicked on
        for (
            index,
            rect,
        ) in self.drawer.empty_tiles_on_plank_index.items():
            if (
                rect.collidepoint(mouse_pos)
                and self.game.shown_player.selected_tile is not None
            ):
                self.game.shown_player.put_tile_on_plank(
                    self.game.shown_player.selected_tile, index
                )

    def handle_button(self, mouse_pos):
        # Check if a button has been clicked on
        for button_text, rect in self.drawer.button_rects.items():
            if rect.collidepoint(mouse_pos):
                match button_text:
                    case "Play":
                        if self.game.shown_player.laying:
                            self.game.shown_player.play_current_move()
                    case "Clear":
                        self.game.shown_player.clear_current_move()
                    case "Swap":
                        if self.game.shown_player.laying:
                            if not self.game.swap_mode:
                                self.game.swap_mode = True  # TODO: implement
                            else:
                                self.game.swap_mode = False
                                self.game.shown_player.swap(
                                    self.game.shown_player.selected_tiles_to_swap
                                )
                    case "Pass":
                        if self.game.shown_player.laying:
                            self.game.shown_player.skip()
                    case "Engine":
                        if self.game.shown_player.laying:
                            for m in self.game.engine.find_possible_moves(
                                self.game.shown_player.plank
                            ):
                                print(m, m.get_direction())
