#! /usr/bin/env python3

# scrabble.py is not installed in our python/site-packages directory.
# We will add the following lines to be able to import scrabble.py from our
# test directory.
import sys
sys.path.append("../src")
sys.path.append("src")

import scrabble_lib

DATA_DIR = "data"
DICTIONARY_FILE = "francais.txt"
DISTRIBUTION_FILE = "french_scrabble_distribution_with_points.csv"

if __name__ == "__main__":
    letter_set, letter_points = scrabble_lib.load_distribution_file(
        "{}/{}".format(DATA_DIR, DISTRIBUTION_FILE))

    if not letter_set:
        exit(1)

    letters = scrabble_lib.generate_random_input(letter_set)
    print(letters)

    word_map = scrabble_lib.load_dictionary_file("{}/{}".format(
        DATA_DIR, DICTIONARY_FILE))

    best_words = scrabble_lib.find_best(letter_points, word_map, letters)
    print(best_words)
    if best_words:
        print("Points:", scrabble_lib.count_points(letter_points,
                                                   best_words[0]))
