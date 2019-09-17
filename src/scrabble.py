#! /usr/bin/env python3

import os
from random import shuffle
import sys
import unidecode


SET_SIZE = 7

def load_distribution_file(file_name):
    '''
    Loads a csv file containing the letters with their number and points.
    The file contains a header: "letter,number,points" and last line ends
    with "\n".
    Returns two dictionaries formatted as: {letter: number} and {letter: points}
    '''
    return_letter_set = {}
    letter_points = {}

    if not os.path.isfile(file_name):
        print("File {} not found".format(file_name), file=sys.stderr)
    else:
        with open(file_name, "r") as csv_file:
            letter_set = csv_file.read().split("\n")

        # Get rid of header and extra blank line
        letter_set = letter_set[1:-1]
        for line in letter_set:
            line = line.split(",")
            return_letter_set[line[0]] = int(line[1])
            letter_points[line[0]] = int(line[2])

    return return_letter_set, letter_points

def load_dictionary_file(file_name):
    '''
    Return the list of words and a dict formatted as: letters_used => [words]
    '''
    return_word_list = []
    word_map = {}

    if not os.path.isfile(file_name):
        print("File {} not found".format(file_name), file=sys.stderr)
    else:
        with open(file_name, "r", encoding="iso-8859-1") as dictionary_file:
            word_list = dictionary_file.read().split("\n")

        for word in word_list:
            if word: # Filter out empty strings
                return_word_list.append(word)
                letters_used = "".join(sorted(unidecode.unidecode(word).upper()))
                if not letters_used in word_map:
                    word_map[letters_used] = [word]
                else:
                    word_map[letters_used].append(word)

    return return_word_list, word_map

def generate_random_input(letter_set):
    '''
    Takes a set/dict of letters {letter:(number,points)} and returns
    SET_SIZE letters picked from that set.
    '''
    pool = []

    # Init pool
    for l, n in letter_set.items():
        for _ in range(n):
            pool.append(l)

    shuffle(pool)

    return pool[:SET_SIZE]

def sort_letters_by_points(letter_points, letters):
    return sorted(letters, key=lambda l: letter_points.get(l, 0))

def sort_all_letters_by_points(letter_points):
    return sorted(letter_points, key=lambda l: letter_points.get(l, 0))

def find_best(word_map, letters):
     pass
