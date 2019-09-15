#! /usr/bin/env python3

import os
import sys

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
