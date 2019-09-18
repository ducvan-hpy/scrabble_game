#! /usr/bin/env python3

# scrabble.py is not installed in our python/site-packages directory.
# We will add the following lines to be able to import scrabble.py from our
# test directory.
import sys
sys.path.append("../src")
sys.path.append("src")

from scrabble import (count_points, find_best, generate_random_input,
                      load_dictionary_file, load_distribution_file,
                      sort_all_letters_by_points, sort_letters_by_points)

DATA_DIR = "data"
DICTIONARY_FILE = "francais.txt"
DISTRIBUTION_FILE = "french_scrabble_distribution_with_points.csv"

if __name__ == "__main__":
    letter_set, letter_points = load_distribution_file("{}/{}".format(
        DATA_DIR, DISTRIBUTION_FILE))

    if not letter_set:
        exit(1)

    letters = generate_random_input(letter_set)
    print(letters)

    word_list, word_map = load_dictionary_file("{}/{}".format(DATA_DIR, DICTIONARY_FILE))

    best_words = find_best(letter_points, word_map, letters)
    print(best_words)
    if best_words:
        print("Points:", count_points(letter_points, best_words[0]))
