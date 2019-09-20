#! /usr/bin/env python3

from datetime import datetime
import scrabble_lib
import time

N_PLAYERS = 2


class Player:
    def  __init__(self, name):
        self._name = name
        self._letters = []
        self._points = 0

    def get_name(self):
        return self._name

    def get_letters(self):
        return self._letters

    def get_number_letters(self):
        return len(self._letters)

    def get_points(self):
        return self._points

    def add_letters(self, new_letters):
        self._letters += new_letters

    def remove_letters(self, removed_letters):
        for l in removed_letters:
            try:
                self._letters.remove(l)
            except ValueError:
                print("Cannot remove letter {} from {}"
                      .format(l, self._letters))


class Game:
    def __init__(self, dictionary_file, distribution_file):
        self.letter_set, self.letter_points = \
            scrabble_lib.load_distribution_file(distribution_file)
        self.n_tiles = sum(self.letter_set.values())
        log_action("Start game with {} tiles".format(self.n_tiles))
        self.word_map = scrabble_lib.load_dictionary_file(dictionary_file)

        # Named player "1", "2", "3"...
        self.players = [Player(i + 1) for i in range(N_PLAYERS)]
        self.player_turn = 0 # index of the player to play next

    def current_player(self):
        return self.players[self.player_turn]

    def next_player(self):
        self.player_turn += 1
        self.player_turn %= N_PLAYERS

    def is_over(self):
        '''
        Return True if no more tiles to pick
        '''
        return self.n_tiles <= 0

    def remove_letters_from_set(self, removed_letters):
        for l in removed_letters:
            self.letter_set[l] -= 1
            self.n_tiles -= 1

    def current_player_pick_letters(self):
        player = self.current_player()
        n_letters = scrabble_lib.SET_SIZE - player.get_number_letters()
        letters = scrabble_lib.generate_random_input(self.letter_set, n_letters)
        self.remove_letters_from_set(letters)
        player.add_letters(letters)
        log_action("Player {} has picked {}".format(player.get_name(), letters))

    def start_game(self):
        for _ in range(N_PLAYERS):
            self.current_player_pick_letters()
            self.next_player()

    def play(self):
        self.start_game()


def log_action(message):
        print(message)
