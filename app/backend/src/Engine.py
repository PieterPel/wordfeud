from Trie import Trie
from Move import Move
import copy


class Engine:
    ALL_LETTER_LIST = [chr(letter) for letter in range(ord("A"), ord("Z") + 1)]

    def __init__(self, board):
        """
        Initializes the Engine object.

        Args:
            board (Board): The board object used by the engine.
        """
        self.board = board
        self.trie = Trie(board.WORD_SET)

    def find_possible_moves(self, plank) -> set:
        """
        Finds all possible moves on the game board for the given plank.

        Args:
            plank: The current state of the game board.

        Returns:
            A set of possible moves that can be made on the game board.

        """
        anchors = self.get_anchors()
        vertical_dict = self.get_verticality_allowed(anchors, plank)
        extension_dict = self.get_left_extension_dict(anchors, plank)

        moves = []
        # Horizontal moves for normal board
        moves.extend(
            self.get_horizontal_moves(
                anchors, vertical_dict, extension_dict, plank
            )
        )

        print("Should start the turned board now")

        # Horizontal moves for turned board
        # TODO add back in since it should work
        # vertical_dict = {
        #     (self.board.LENGTH - 1 - y, self.board.HEIGHT - 1 - x): constraints
        #     for (x, y), constraints in vertical_dict.items()
        # }
        # anchors = set(vertical_dict.keys())
        turned_board = self.board.get_turned_board()

        # Temporarily change the board (very ugly code I know)
        normal_board = self.board
        self.board = turned_board
        anchors = self.get_anchors()
        vertical_dict = self.get_verticality_allowed(anchors, plank)
        extension_dict = self.get_left_extension_dict(anchors, plank)
        normal_moves = [
            move.get_turned_move()
            for move in self.get_horizontal_moves(
                anchors, vertical_dict, extension_dict, plank
            )
        ]
        self.board = normal_board

        moves.extend(normal_moves)

        return moves

    def get_anchors(self) -> set:
        """
        Get the set of anchor coordinates on the board.

        An anchor coordinate is an empty cell adjacent to a filled cell.

        Returns:
            set: A set of anchor coordinates.
        """
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
                and self.coordinates_on_board(neighbor)
            ]
            anchors.update(empty_neighbors)

        return anchors

    def get_verticality_allowed(self, anchors, plank) -> dict:
        """Gets a dictionary containing the letters of the plank that
        are allowed at the anchors by verticality

        Args:
            anchors (list): _description_
            plank (Plank): _description_

        Returns:
            dict: _description_
        """
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
            while y - dy >= 0 and self.board[(x, y - dy)].filled:
                down += self.board[(x, y - dy)].tile.letter
                dy += 1

            # If nothing up and down everything is allowed
            if up == "" and down == "":
                if " " in plank.letters:
                    allowed_letters = self.ALL_LETTER_LIST
                else:
                    allowed_letters = plank.letters
            else:
                # If word is allowed, add to dictionary
                allowed_letters = []
                for tile in plank:
                    # Determine which letters to check
                    if tile is None:
                        continue
                    elif tile.blank:
                        letters = self.ALL_LETTER_LIST
                    else:
                        letters = [tile.letter]

                    # Cycle over the letters and check which are allowed
                    for letter in letters:
                        formed_word = f"{up[::-1]}{letter}{down}"
                        if formed_word in self.board.WORD_SET:
                            allowed_letters.append(letter)
            allowed[anchor] = allowed_letters

            print(f"For anchor {anchor}, {allowed_letters} are allowed")

        return allowed

    def get_left_extension_dict(self, anchors, plank) -> dict:
        """
        Returns a dictionary containing the left extensions for each anchor position.

        Args:
            anchors (list): A list of anchor positions.
            plank (str): The current state of the game board.

        Returns:
            dict: A dictionary where the keys are anchor positions and the values are tuples
                  containing the fixed extensions and the maximum length of the extensions.
        """
        extension_dict = dict()

        for anchor in anchors:
            fixed, max_length = self.get_left_extensions(
                anchor, plank, anchors
            )

            extension_dict[anchor] = (fixed, max_length)

        return extension_dict

    def get_horizontal_moves(
        self, anchors, vertical_dict, extension_dict, plank
    ) -> set:
        """
        Get all possible horizontal moves for the given anchors, vertical dictionary,
        extension dictionary, and plank.

        Parameters:
        anchors (list): List of anchor positions.
        vertical_dict (dict): Dictionary containing vertical words.
        extension_dict (dict): Dictionary containing extension information for each anchor.
        plank (Plank): The plank object representing the game board.

        Returns:
        set: Set of all possible horizontal moves.
        """
        moves = []

        lengths = set()
        for anchor in anchors:
            lengths.add(extension_dict[anchor][1])
        max_length = max(lengths)

        all_extensions = self.get_possible_left_plank_extensions(
            max_length, plank
        )

        # Loop over all anchors
        for anchor in anchors:
            print(f"Now checking anchor: {anchor}")
            # Get possible left extensions
            # (
            #     left_extension_fixed,
            #     left_extensions_plank,
            # ) = self.get_left_extensions(anchor, plank, anchors)

            left_extension_fixed, max_extension_length = extension_dict[anchor]
            left_extensions_plank = set(
                x if len(x) < max_extension_length else ""
                for x in all_extensions
            )

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

    def get_left_extensions(self, anchor, plank, anchors):
        x, y = anchor
        laid_on_left = ""
        possible_with_plank = {""}

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
            # possible_with_plank = self.get_possible_left_plank_extensions(
            #     dx - 1, plank
            # )

        return laid_on_left[::-1], dx - 1

    def get_possible_left_plank_extensions(self, max_length, plank) -> set:
        """
        Generates all possible left plank extensions for a given maximum length and plank.

        Args:
            max_length (int): The maximum length of the extensions.
            plank (Plank): The plank object representing the current state of the game.

        Returns:
            set: A set of all possible left plank extensions.
        """
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
        if " " in letters_remaining_on_plank:
            remaining_set = set(self.ALL_LETTER_LIST)
        else:
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
            num_non_fixed <= len(letters_remaining_on_plank)
            or self.board[(x + dx, y)].filled
        ):
            scanned_coords = (x + dx, y)
            dx += 1

            # Check if there already is a tile
            if self.board[scanned_coords].filled:
                laid_down.append(self.board[scanned_coords].tile.letter)
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
        extensions = anchor_options_set
        dead_extensions = set()

        # Look at right extensions until the maximum possible depth
        for index, (fixed_letter, vertical_allowed_tiles) in enumerate(
            zip(laid_down, vertically_allowed)
        ):
            new_extensions = set()
            infeasible_extensions = set()

            # Loop over all already available prefixes
            for extension in extensions:
                # if len(extension) - 2 < index: # Had this here first
                if extension in dead_extensions:
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

                    if options == set():
                        dead_extensions.add(extension)

                    # Add the options
                    for option in options:
                        new_extensions.add(extension + option)

                # If there is a tile already laid down, the prefix actually can't be laid down
                else:
                    infeasible_extensions.add(extension)
                    new_extensions.add(extension + fixed_letter)

            # Add new extensions and remove infeasible ones
            extensions.update(new_extensions)
            extensions -= infeasible_extensions

        # Generate the possible words
        for extension in extensions:
            word = left_extension + extension
            if word in self.board.WORD_SET:
                legal_words.add(word)

        return legal_words

    # TODO: Can probably be made prettier/more efficient
    def turn_words_into_moves(
        self, words, anchor, plank, left_extension, fixed: bool
    ) -> list:
        """
        Converts a list of words into a list of moves based on the given parameters.

        Args:
            words (list): A list of words to be converted into moves.
            anchor (tuple): The coordinates of the anchor tile.
            plank (Plank): The plank object representing the current state of the game board.
            left_extension (str): The left extension of the word being formed.
            fixed (bool): Indicates whether the left extension is fixed or not.

        Returns:
            list: A list of Move objects representing the possible moves.

        """
        moves = []
        x, y = anchor

        # Fixed left extension => all tiles on the plank are available to form the word
        if fixed:
            for word in words:
                if len(word) < 2:
                    continue

                tiles = copy.copy(plank.tile_list)

                move = Move()
                dx = 0
                part_to_lay_down = word[len(left_extension) :]
                for letter in part_to_lay_down:
                    if self.board[(x + dx, y)].filled:
                        dx += 1
                        continue

                    tile = grab_letter_from_tile_list(tiles, letter)
                    move[tile] = (x + dx, y)
                    dx += 1

                moves.append(move)

        # Else first need to lay down the left extension
        else:
            for word in words:
                if len(word) < 2:
                    continue

                tiles = copy.copy(plank.tile_list)
                move = Move()
                dx = -len(left_extension)

                for letter in word:
                    print(x + dx, y, letter)
                    if self.board[(x + dx, y)].filled:
                        dx += 1
                        continue

                    tile = grab_letter_from_tile_list(tiles, letter)
                    move[tile] = (x + dx, y)
                    dx += 1

                moves.append(move)
        return moves

    def coordinates_on_board(self, coords: tuple):
        """
        Check if the given coordinates are within the boundaries of the game board.

        Args:
            coords (tuple): The coordinates to check, in the format (x, y).

        Returns:
            bool: True if the coordinates are on the board, False otherwise.
        """
        x, y = coords
        if x < 0 or y < 0:
            return False
        elif x >= self.board.LENGTH or y >= self.board.HEIGHT:
            return False
        else:
            return True


def grab_letter_from_tile_list(tile_list, letter):
    """
    Grabs a letter from the tile list and removes it from the list.

    Args:
        tile_list (list): The list of tiles to search for the letter.
        letter (str): The letter to grab from the tile list.

    Returns:
        Tile: The tile object containing the grabbed letter.

    Raises:
        ValueError: If the letter is not found in the tile list or a blank tile is not available.
    """
    # Also removes the letter from the list
    # Check for the letter on the tiles
    for tile in tile_list:
        if tile is None:
            continue

        if tile.blank:
            blank = tile

        if tile.letter == letter:
            tile_list.remove(tile)
            return tile

    # Return a blank if letter not found and available
    try:
        tile_list.remove(blank)
        blank_copy = copy.copy(blank)
        blank_copy.letter = (
            letter  # TODO: check if this isn't very memory intensive
        )
        return blank_copy
    except UnboundLocalError:
        print(f"Letter: {letter}, list: {tile_list}")
        raise ValueError("This list cannot provide that letter or a blank")
