#! /usr/bin/env python3

# scrabble.py is not installed in our python/site-packages directory.
# We will add the following lines to be able to import scrabble.py from our
# test directory.
import sys
sys.path.append("../src")
sys.path.append("src")

import os.path
import scrabble_lib

DATA_DIR = "../data"
DICTIONARY_FILE = "francais.txt"
DISTRIBUTION_FILE = "french_scrabble_distribution_with_points.csv"

if __name__ == "__main__":
    dictionary_file = "{}/{}".format(DATA_DIR, DICTIONARY_FILE)
    distribution_file = "{}/{}".format(DATA_DIR, DISTRIBUTION_FILE)

    while not os.path.exists(dictionary_file) or \
       not os.path.exists(distribution_file):
        print("Cannot load {} or {}".format(dictionary_file, distribution_file),
              file=sys.stderr)

        data_dir = input("Please specify data dir\n> ")

        dictionary_file = "{}/{}".format(data_dir, DICTIONARY_FILE)
        distribution_file = "{}/{}".format(data_dir, DISTRIBUTION_FILE)


    letter_set, letter_points = scrabble_lib.load_distribution_file(
        distribution_file)

    if not letter_set:
        exit(1)

    letters = scrabble_lib.generate_random_input(letter_set)
    print("Letters:", letters)

    word_map = scrabble_lib.load_dictionary_file(dictionary_file)

    best_word, points = scrabble_lib.find_best(letter_points, word_map, letters)
    print("Best word:", best_word)
    print("Points:", points)
