"""
Source: https://albertauyeung.github.io/2020/06/15/python-trie.html/
"""

import copy


class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}


class Trie(object):
    """The trie object"""

    def __init__(self, word_set=None):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        if word_set is None:
            word_set = set()

        self.root = TrieNode("")

        for word in word_set:
            self.insert(word)

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1

    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root

        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)

    def get_children(self, prefix: str) -> set:
        node = self.root

        # Check if the prefix is in the trie
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        return set(node.children.keys())

    def generate_prefix_combinations(
        self, max_length, available_letters
    ) -> set:
        """
        Generate all possible prefixes using the available letters,
        ensuring that each prefix can form at least one word by adding
        at least one word to it.

        Args:
            - max_length: maximum length of the prefixes
            - available_letters: set of available letters

        Returns:
            List of prefixes
        """
        output = {""}

        length = 1
        while length <= (max_length):
            new_prefixes = set()

            # Go one level deeper, using already existing output
            for prefix in output:
                # Find the remaining letters
                used_letters = [letter for letter in prefix]
                remaining_letters = copy.deepcopy(available_letters)

                for letter in used_letters:
                    if letter not in remaining_letters:
                        remaining_letters.remove(" ")
                    else:
                        remaining_letters.remove(letter)

                # Cycle over the remaing letters
                for letter in remaining_letters:
                    if self.query(prefix + letter) != []:
                        new_prefixes.add(prefix + letter)
                    # Check for a blanc
                    elif letter == " ":
                        for child in self.get_children(prefix):
                            new_prefixes.add(prefix + child)

            output.update(new_prefixes)
            length += 1

        return output
