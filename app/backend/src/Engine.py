from Trie import Trie
from Move import Move
import copy


class Engine:
    def __init__(self, board):
        self.board = board
        self.trie = Trie(board.WORD_SET)

    def find_possible_moves(self, plank) -> set:
        anchors = self.get_anchors()
        vertical_dict = self.get_verticality_allowed(anchors, plank)

        def get_horizontal_moves(anchors, vertical_dict) -> set:
            moves = []

            # Loop over all anchors
            for anchor in anchors:
                # Get possible left extensions
                (
                    left_extension_fixed,
                    left_extensions_plank,
                ) = self.get_left_extensions(anchor, plank, anchors)

                # Check if there is a fixed left_extension
                if left_extension_fixed != "":
                    words = self.get_possible_words_from_left_extension(
                        anchor,
                        plank.letters,
                        left_extension_fixed,
                        vertical_dict,
                    )

                    # Turn these words into Moves
                    moves.extend(
                        self.turn_words_into_moves(
                            words,
                            anchor,
                            plank,
                            left_extension_fixed,
                            fixed=True,
                        )
                    )

                # Else there may be possiblities with the plank or without a left extension
                else:
                    print(
                        f"# of left extensions: {len(left_extensions_plank)}"
                    )
                    print(left_extensions_plank)
                    for extension in left_extensions_plank:
                        # Figure out which letters remain on the plank
                        used_letters = [letter for letter in extension]
                        remaining_letters = copy.copy(plank.letters)
                        for letter in used_letters:
                            if letter in remaining_letters:
                                remaining_letters.remove(letter)
                            else:
                                remaining_letters.remove(" ")

                        # Update the word list
                        possible_words = (
                            self.get_possible_words_from_left_extension(
                                anchor,
                                remaining_letters,
                                extension,
                                vertical_dict,
                            )
                        )

                        if possible_words != set():
                            moves.extend(
                                self.turn_words_into_moves(
                                    possible_words,
                                    anchor,
                                    plank,
                                    extension,
                                    fixed=False,
                                )
                            )

            return moves

        moves = []
        # Horizontal moves for normal board
        moves.extend(get_horizontal_moves(anchors, vertical_dict))

        # Horizontal moves for turned board
        anchors = set(
            (self.board.LENGTH - 1 - y, self.board.HEIGHT - 1 - x)
            for (x, y) in anchors
        )
        vertical_dict = {
            (self.board.LENGTH - 1 - y, self.board.HEIGHT - 1 - x): constraints
            for (x, y), constraints in vertical_dict.items()
        }
        turned_board = self.board.get_turned_board()

        # Temporarily change the board (very ugly code I know)
        normal_board = self.board
        self.board = turned_board
        normal_moves = [
            move.get_turned_move()
            for move in get_horizontal_moves(anchors, vertical_dict)
        ]
        self.board = normal_board

        moves.extend(normal_moves)

        return moves

    def get_anchors(self) -> set:
        anchors = set()

        # Check if middle is filled, else add to anchors
        middle = self.board.MIDDLE
        if not self.board[middle].filled:
            anchors.add(middle)

        # Loop over all filled coordinates and add empty neighbors
        for x, y in self.board.filled_coordinates:
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            empty_neighbors = [
                neighbor
                for neighbor in neighbors
                if not self.board[neighbor].filled
            ]
            anchors.update(empty_neighbors)

        return anchors

    def get_verticality_allowed(self, anchors, plank) -> dict:
        allowed = dict()

        # Loop over all anchors
        for anchor in anchors:
            x, y = anchor

            # Scan up
            dy = 1
            up = ""
            while (
                y + dy < self.board.HEIGHT and self.board[(x, y + dy)].filled
            ):
                up += self.board[(x, y + dy)].tile.letter
                dy += 1

            # Scan down
            dy = 1
            down = ""
            while y + dy >= 0 and self.board[(x, y + dy)].filled:
                down += self.board[(x, y + dy)].tile.letter
                dy -= 1

            # TODO: I think I am still approaching the blanks wrongly, the blank can only be certain letters from the vertical constraints
            # TODO: Hence that should also be taken into account when forming the word horizontally
            # If nothing up and down or there is a blank, everything is allowed
            if (up == "" and down == "") or " " in plank.letters:
                allowed[anchor] = plank.letters
            else:
                # If word is allowed, add to dictionary
                allowed_words = []
                for tile in plank:
                    letter = tile.letter
                    formed_word = f"{up[::-1]}{letter}{down}"
                    if formed_word in self.board.WORD_SET:
                        allowed_words.append(letter)
                allowed[anchor] = allowed_words

        return allowed

    def get_left_extensions(self, anchor, plank, anchors):
        x, y = anchor
        laid_on_left = ""
        possible_with_plank = [""]

        # Check if anchor on the left side of the board
        if x == 0:
            return laid_on_left, possible_with_plank

        dx = 1
        # Filled tile to the left
        if self.board[(x - dx, y)].filled:
            while self.board[(x - dx, y)].filled:
                letter = self.board[(x - dx, y)].tile.letter
                laid_on_left += letter
                dx += 1
        # Empty tile to the left
        else:
            # Scan until you seen another anchor, at the edge or not enough tiles on the plank
            while (
                (x - dx, y) not in anchors
                and x - dx != 0
                and dx < len(plank.letters)
            ):
                dx += 1
            possible_with_plank = self.get_possible_left_plank_extensions(
                dx, plank
            )

        return laid_on_left, possible_with_plank

    def get_possible_left_plank_extensions(
        self, max_length, plank
    ) -> list[str]:
        return self.trie.generate_prefix_combinations(
            max_length, plank.letters
        )

    def get_possible_words_from_left_extension(
        self,
        anchor,
        letters_remaining_on_plank,
        left_extension,
        vertically_allowed_dict,
    ) -> set:
        legal_words = set()

        # Check if there is an existing intersection between children of left_extension node and letters remaining on plank else return an empty set
        remaining_set = set(letters_remaining_on_plank)
        children_set = self.trie.get_children(left_extension)
        allowed_set = set(vertically_allowed_dict[anchor])
        anchor_options_set = remaining_set.intersection(
            children_set
        ).intersection(allowed_set)
        if anchor_options_set == set():
            return legal_words

        x, y = anchor

        # Scan rightward to pick up the fixed tiles and vertical constraints
        dx = 1
        num_non_fixed = 0
        laid_down = []
        vertically_allowed = []

        # Keep scanning until the edge of the board or the plank is empty and there are no laid down tiles to the left
        while x + dx < self.board.LENGTH and (
            num_non_fixed
            <= len(
                letters_remaining_on_plank or self.board[(x + dx, y)].filled
            )
        ):
            scanned_coords = (x + dx, y)

            # Check if there already is a tile
            if self.board[scanned_coords].filled:
                laid_down.append(self.board[(x + dx, y)].tile.letter)
            else:
                num_non_fixed += 1
                laid_down.append(None)

            # Check if there is a constrained anchor
            if scanned_coords in vertically_allowed_dict.keys():
                vertically_allowed.append(
                    vertically_allowed_dict[scanned_coords]
                )
            else:
                vertically_allowed.append(letters_remaining_on_plank)

        # First options are the possibilities at the anchor
        extensions = set(option for option in anchor_options_set)

        # Look at right extensions until the maximum possible depth
        for index, (fixed_letter, vertical_allowed_tiles) in enumerate(
            zip(laid_down, vertically_allowed)
        ):
            # Loop over all already available prefixes
            for extension in extensions:
                # Skip if the prefix has a length that is too short i.e. had no options in previous run
                if len(extension) - 2 < index:
                    continue

                # If there is no tile already laid down
                if fixed_letter is None:
                    # Figure out remaining letters
                    letters_in_prefix = [letter for letter in extension]
                    fixed_tiles_passed = laid_down[: index + 1]
                    remaining_letters = copy.deepcopy(
                        letters_remaining_on_plank
                    )

                    for letter in letters_in_prefix:
                        if letter in fixed_tiles_passed:
                            fixed_tiles_passed.remove(letter)
                        elif letter not in remaining_letters:
                            remaining_letters.remove(" ")
                        else:
                            remaining_letters.remove(letter)

                    # Get the possible options to lay down
                    if " " in remaining_letters:
                        options = set(vertical_allowed_tiles).intersection(
                            self.trie.get_children(left_extension + extension)
                        )
                    else:
                        options = (
                            set(vertical_allowed_tiles)
                            .intersection(set(remaining_letters))
                            .intersection(
                                self.trie.get_children(
                                    left_extension + extension
                                )
                            )
                        )

                    # Add the options
                    for option in options:
                        extensions.add(extension + option)

                # If there is a tile already laid down, the prefix actually can't be laid down
                else:
                    extensions.remove(extension)
                    extensions.add(extension + fixed_letter)

        # Generate the possible words
        for extension in extensions:
            word = left_extension + extension
            if word in self.board.WORD_SET:
                legal_words.add(word)

        return legal_words

    # TODO: Can probably be made prettier/more efficient
    @staticmethod
    def turn_words_into_moves(
        words, anchor, plank, left_extension, fixed: bool
    ) -> list:
        moves = []
        x, y = anchor

        # Fixed left extension => all tiles on the plank are available to form the word
        if fixed:
            for word in words:
                tiles = copy.copy(plank.tile_list)

                move = Move()
                dx = 0
                part_to_lay_down = word[len(left_extension) :]
                for letter in part_to_lay_down:
                    tile = grab_letter_from_tile_list(tiles, letter)
                    move[tile] = (x + dx, y)
                    dx += 1

                moves.append(move)

        # Else first need to lay down the left extension
        else:
            for word in words:
                tiles = copy.copy(plank.tile_list)
                move = Move()
                dx = -len(left_extension)

                for letter in word:
                    tile = grab_letter_from_tile_list(tiles, letter)
                    move[tile] = (x + dx, y)
                    dx += 1

                moves.append(move)
        return moves


def grab_letter_from_tile_list(tile_list, letter):
    # Also removes the letter from the list
    # Check for the letter on the tiles
    for tile in tile_list:
        if tile.letter == " ":
            blank = tile

        if tile.letter == letter:
            tile_list.remove(tile)
            return tile

    # Return a blank if letter not found and avalable
    if " " in tile_list:
        tile_list.remove(blank)
        return blank
    else:
        raise ValueError("This list cannot provide that letter or a blank")
