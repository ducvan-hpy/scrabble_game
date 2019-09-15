#! /usr/bin/env python3

# scrabble.py is not installed in our python/site-packages directory.
# We will add the following lines to be able to import scrabble.py from our
# test directory.
import sys
sys.path.append("../src")
sys.path.append("src")

from scrabble import load_distribution_file

DATA_DIR = "data"
DICTIONARY = "francais.txt"
DISTRIBUTION_FILE = "french_scrabble_distribution_with_points.csv"

if __name__ == "__main__":
    letter_set = load_distribution_file("{}/{}".format(DATA_DIR,
                                                       DISTRIBUTION_FILE))

    if not letter_set:
        exit(1)
    else:
        print(letter_set)
