from Board import Board
from Trie import Trie
import timeit

board = Board()
set = board.WORD_SET
trie = Trie(set)

letters = ["A", "B", "C", "D", "E", " ", " "]

string_to_compare = "BAD"
length = 7

execution_time = timeit.timeit(
    lambda: trie.generate_prefix_combinations(length, letters), number=1
)
print(f"Execution time: {execution_time} seconds")
