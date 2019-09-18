#! /usr/bin/env python3

import os
from random import shuffle
import sys
import unidecode


SET_SIZE = 7
BLANK_TILE_NAME = "blank"
MAX_BLANK_TILES = 2

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
    Return the list of words and a dictionary formatted like:
    word_map: {len(word): {letters_used: [words]}}
    For example:
    {
        1: {A: [A]},
        2: {
              AB: [AB, BA],
              BC: [BC, CB],
           },
        ...
    }
    As we will handle words where the length is SET_SIZE letters max,
    we will not store words where the len(word) > SET_SIZE.
    '''
    return_word_list = []
    word_map = {}

    if not os.path.isfile(file_name):
        print("File {} not found".format(file_name), file=sys.stderr)
    else:
        with open(file_name, "r", encoding="iso-8859-1") as dictionary_file:
            word_list = dictionary_file.read().split("\n")

        for word in word_list:
            # Filter out empty strings and long words
            if word and len(word) <= SET_SIZE:
                return_word_list.append(word)
                wword_length = len(word)
                letters_used = "".join(sorted(unidecode.unidecode(word).upper()))
                if not wword_length in word_map:
                    word_map[wword_length] = {}
                if not letters_used in word_map[wword_length]:
                    word_map[wword_length][letters_used] = [word]
                else:
                    word_map[wword_length][letters_used].append(word)

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

def find_words(word_map, letters):
    '''
    Returns words that can be formed from letters.
    '''
    wword_length = len(letters)
    selected_letters = "".join(sorted(letters))
    print("find_words", letters)
    return word_map[wword_length].get(selected_letters)

def find_best_with_blank(letter_points, word_map, letters):
    # All letters without blank
    all_letters = list(letter_points)
    all_letters.remove(BLANK_TILE_NAME)

    word_found = None
    if letters.count(BLANK_TILE_NAME) == MAX_BLANK_TILES:
        for l in all_letters:
            tmp_letters = list(letters)
            tmp_letters.remove(BLANK_TILE_NAME)
            tmp_letters.append(l)

            for l in all_letters:
                tmp_letters_2 = list(tmp_letters)
                tmp_letters_2.remove(BLANK_TILE_NAME)
                tmp_letters_2.append(l)

                word_found = find_words(word_map, tmp_letters_2)
                if word_found:
                    return word_found
    else:
        for l in all_letters:
            tmp_letters = list(letters)
            tmp_letters.remove(BLANK_TILE_NAME)
            tmp_letters.append(l)

            word_found = find_words(word_map, tmp_letters)
            if word_found:
                break

    return word_found

def get_subsets(letter_points, letters):
    subsets = []

    # Sort by points, remove letters with lowest points first
    sorted_letters = sort_letters_by_points(letter_points, letters)

    for l in sorted_letters:
        tmp_letters = list(letters)
        tmp_letters.remove(l)
        subsets.append(tmp_letters)

    return subsets

def find_best_subsets(letter_points, word_map, letters):
    subsets1 = get_subsets(letter_points, letters)
    subsets2 = []

    word_found = None
    while not word_found and subsets1:
        for tmp_letters in subsets1:
            word_found = find_words(word_map, tmp_letters)
            if word_found:
                return word_found
            subsets2 += get_subsets(letter_points, tmp_letters)

        subsets1 = subsets2
        subsets2 = []

    return None

def find_best(letter_points, word_map, letters):
    word_found = None
    if BLANK_TILE_NAME in letters:
        word_found = find_best_with_blank(letter_points, word_map, letters)
    else:
        word_found = find_words(word_map, letters)

        if not word_found:
            word_found = find_best_subsets(letter_points, word_map, letters)

    return word_found
