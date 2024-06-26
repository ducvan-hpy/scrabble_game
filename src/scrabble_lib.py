#! /usr/bin/env python3

import os
from random import shuffle
import sys
import unidecode


SET_SIZE = 7
BLANK_TILE_NAME = "blank"
MIN_WORD_SIZE = 2
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
    word_map = {}

    if not os.path.isfile(file_name):
        print("File {} not found".format(file_name), file=sys.stderr)
    else:
        with open(file_name, "r", encoding="iso-8859-1") as dictionary_file:
            word_list = dictionary_file.read().split("\n")

        for word in word_list:
            # Filter out empty strings and short words and long words
            l_word = len(word)
            if word and l_word >= MIN_WORD_SIZE and l_word <= SET_SIZE:
                letters_used = "".join(sorted(unidecode.unidecode(word).
                                              upper()))
                if not l_word in word_map:
                    word_map[l_word] = {}
                if not letters_used in word_map[l_word]:
                    word_map[l_word][letters_used] = [word]
                else:
                    word_map[l_word][letters_used].append(word)

    return word_map

def generate_random_input(letter_set, nletters=SET_SIZE):
    '''
    Takes a set/dict of letters {letter:(number,points)} and returns
    nletters letters (SET_SIZE by default) picked from that set.
    '''
    pool = []

    # Init pool
    for l, n in letter_set.items():
        for _ in range(n):
            pool.append(l)

    shuffle(pool)

    return pool[:nletters]

def sort_letters_by_points(letter_points, letters):
    return sorted(letters, key=lambda l: letter_points.get(l, 0))

def sort_all_letters_by_points(letter_points):
    return sorted(letter_points, key=lambda l: letter_points.get(l, 0))

def find_words(word_map, letters):
    '''
    Returns words that can be formed from letters.
    '''
    word_length = len(letters)
    selected_letters = "".join(sorted(letters))
    if word_length < MIN_WORD_SIZE:
        return None
    return word_map[word_length].get(selected_letters)

def find_best_with_blank(letter_points, word_map, letters):
    # All letters without blank
    all_letters = list(letter_points)
    all_letters.remove(BLANK_TILE_NAME)

    word_found = None

    # Handle case with 2 blank tiles
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
    words_found = []
    while subsets1:
        for tmp_letters in subsets1:
            if BLANK_TILE_NAME in tmp_letters:
                word_found = find_best_with_blank(letter_points, word_map,
                                                  tmp_letters)
            else:
                word_found = find_words(word_map, tmp_letters)

            if word_found:
                words_found += word_found
            subsets2 += get_subsets(letter_points, tmp_letters)

        subsets1 = subsets2
        subsets2 = []

    return words_found

def count_points(letter_points, word):
    score = 0
    letters = unidecode.unidecode(word).upper()
    for l in letters:
        score += letter_points[l]
    return score

def max_points_word(letter_points, words):
    if not words:
        return None, 0

    word_points = {}
    for word in words:
        word_key = unidecode.unidecode(word).upper()
        if not word_key in word_points:
            word_points[word_key] = count_points(letter_points, word)

    best_word = max(word_points, key=word_points.get)
    return best_word, word_points.get(best_word)

def find_best(letter_points, word_map, letters):
    word_found = []
    # Try to use all letters first
    if BLANK_TILE_NAME in letters:
        words_found = find_best_with_blank(letter_points, word_map, letters)
    else:
        words_found = find_words(word_map, letters)

    # Try to find words using a subset of letters
    if not words_found:
        words_found = find_best_subsets(letter_points, word_map, letters)

    return max_points_word(letter_points, words_found)
