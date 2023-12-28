from os.path import realpath, join, dirname
from unidecode import unidecode

# Get set of all verbs
verb_set = set()
with open(
    realpath(
        join(dirname(__file__), "../wordlists/werkwoorden-infinitief.txt")
    )
) as verb_list:
    for verb in verb_list:
        verb_set.add(unidecode(verb))

# Read every line in word_list.txt
with open(
    realpath(join(dirname(__file__), "../wordlists/wordlist.txt")), "r"
) as word_list, open(
    realpath(join(dirname(__file__), "../wordlists/wordlist-edited.txt")), "w"
) as edited_wordlist:
    for word in word_list:
        # Remove if it has has a capital letter, a digit, hyphen, space or period
        # TODO: some words with hyphens are accepted without the hypen such as zee-egel -> zeeegel
        if any(
            char.isupper() or char.isdigit() or char in ["-", " ", "."]
            for char in word
        ):
            continue

        # TODO: abbreviations are still allowed

        # Convert diecritics to normal letters by converting to unicode
        word = unidecode(word)

        # Remove '
        word = word.replace("'", "")

        # Remove small words (add back manually) and words that are larger than the board
        if len(word[:-1]) < 3 or len(word[:-1]) >= 15:
            continue

        # Add word to edited word list
        edited_wordlist.write(word)

        # Add conjunctive and weird forms form by using the set of verbs
        if word in verb_set and word[-3:-1] == "en":
            edited_wordlist.write(f"{word[:-2]}\n")
            edited_wordlist.write(f"{word[:-1]}den\n")
            edited_wordlist.write(f"{word[:-1]}de\n")

with open(
    realpath(join(dirname(__file__), "../wordlists/two-letter-words.txt")), "r"
) as two_letter_words, open(
    realpath(join(dirname(__file__), "../wordlists/wordlist-edited.txt")), "a"
) as edited_wordlist:
    for word in two_letter_words:
        edited_wordlist.write(word)
