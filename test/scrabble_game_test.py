#! /usr/bin/env python3

# scrabble.py is not installed in our python/site-packages directory.
# We will add the following lines to be able to import scrabble.py from our
# test directory.
import sys
sys.path.append("../src")
sys.path.append("src")

import os.path
import scrabble_game

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

    game = scrabble_game.Game(dictionary_file, distribution_file)

    game.play()
