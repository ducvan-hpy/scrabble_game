#! /usr/bin/env python3

# scrabble.py is not installed in our python/site-packages directory.
# We will add the following lines to be able to import scrabble.py from our
# test directory.
import sys
sys.path.append("../src")
sys.path.append("src")

from scrabble import (generate_random_input, load_dictionary_file,
                      load_distribution_file)

DATA_DIR = "data"
DICTIONARY_FILE = "francais.txt"
DISTRIBUTION_FILE = "french_scrabble_distribution_with_points.csv"

if __name__ == "__main__":
    letter_set = load_distribution_file("{}/{}".format(DATA_DIR,
                                                       DISTRIBUTION_FILE))

    if not letter_set:
        exit(1)

    print(letter_set)

    letters = generate_random_input(letter_set)
    print(letters)

    word_list = load_dictionary_file("{}/{}".format(DATA_DIR, DICTIONARY_FILE))
    print(word_list[-10:])
