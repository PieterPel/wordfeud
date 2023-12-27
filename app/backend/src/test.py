from Board import Board
from Trie import Trie

board = Board()
trie = Trie(word_set=board.WORD_SET)

letters = ["A", "B", "C", "D", "E", "F", "G"]

print(trie.generate_prefix_combinations(7, letters))
