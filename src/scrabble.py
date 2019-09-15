#! /usr/bin/env python3

import os
from random import shuffle
import sys

SET_SIZE = 7

def load_distribution_file(file_name):
    '''
    Loads a csv file containing the letters with their number and points.
    The file contains a header: letter,number,points.
    '''
    return_letter_set = []

    if not os.path.isfile(file_name):
        print("File {} not found".format(file_name), file=sys.stderr)
    else:
        with open(file_name, "r") as csv_file:
            letter_set = csv_file.read().split("\n")

        # Get rid of header and extra blank line
        letter_set = letter_set[1:-1]
        for line in letter_set:
            line = line.split(",")
            return_letter_set.append((line[0], int(line[1]), int(line[2])))

    return return_letter_set

def generate_random_input(letter_set):
    '''
    Takes a set/list of letters (letter,number,points) and returns
    SET_SIZE letters picked from that set.
    '''
    pool = []

    # Init pool
    for lnp in letter_set: # lnp: (letter,number,point)
        for _ in range(lnp[1]):
            pool.append(lnp[0])

    shuffle(pool)

    return pool[:SET_SIZE]
