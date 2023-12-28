import timeit

# Your existing code here...

# Time the function
time = timeit.timeit(
    lambda: trie.generate_prefix_combinations(length, letters), number=1
)
print(f"Execution time: {time} seconds")
