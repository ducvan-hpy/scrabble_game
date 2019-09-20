#! /usr/bin/env python3

from datetime import datetime
import scrabble_lib
import time
import unidecode


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

    def remove_letters(self, letters):
        # Letters removed from _letters, does not countain joker.
        # Will be used to count the total points
        removed_letters = []

        for l in letters:
            try:
                self._letters.remove(l)
                removed_letters.append(l)
            except ValueError:
                # Blank tile used as joker
                self._letters.remove(scrabble_lib.BLANK_TILE_NAME)
                log_action("Player {} used blank tile to replace '{}'".format(
                    self.get_name(), l))

        return removed_letters

    def add_points(self, points):
        self._points += points


class Game:
    def __init__(self, dictionary_file, distribution_file):
        self.letter_set, self.letter_points = \
            scrabble_lib.load_distribution_file(distribution_file)
        self.n_tiles = sum(self.letter_set.values())
        log_action("Start game with {} tiles\n===".format(self.n_tiles))
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

    def current_player_pick_1_letter(self, letter_set):
        player = self.current_player()
        l = None

        while not l or l == scrabble_lib.BLANK_TILE_NAME:
            l = scrabble_lib.generate_random_input(letter_set, 1)[0]
            letter_set[l] -= 1
            log_action("Player {} has picked a '{}' tile".
                       format(player.get_name(), l))

        return l

    def current_player_pick_letters(self):
        player = self.current_player()
        n_letters = scrabble_lib.SET_SIZE - player.get_number_letters()
        letters = scrabble_lib.generate_random_input(self.letter_set, n_letters)
        self.remove_letters_from_set(letters)
        player.add_letters(letters)
        log_action("Player {} has picked {}".format(player.get_name(), letters))

    def setup_game(self):
        # Each player draw 1 tile, the closest to A start the game
        players_start_tile = []
        letter_set = dict(self.letter_set)

        for _ in range(N_PLAYERS):
            l = self.current_player_pick_1_letter(letter_set)
            players_start_tile.append(l)
            self.next_player()

        min_tile = min(players_start_tile)
        self.player_turn = players_start_tile.index(min_tile)

        player = self.current_player()
        log_action("Player {} has the tile closest to 'A', he will be the "
                   "first player to play\n===".format(player.get_name()))

        for _ in range(N_PLAYERS):
            self.current_player_pick_letters()
            self.next_player()

    def end_game(self):
        for _ in range(N_PLAYERS):
            player = self.current_player()
            log_action("Player {} hand: {}".format(player.get_name(),
                                                   player.get_letters()))

            log_action("Player {} got {} points".format(player.get_name(),
                                                        player.get_points()))
            self.next_player()

    def play(self):
        self.setup_game()

        while not self.is_over():
            player = self.current_player()
            log_action("Player {} hand: {}".format(player.get_name(),
                                                   player.get_letters()))

            best_words = scrabble_lib.find_best(self.letter_points,
                                                self.word_map,
                                                player.get_letters())

            best_word = unidecode.unidecode(best_words[0]).upper()
            removed_letters = player.remove_letters(best_word)
            points = scrabble_lib.count_points(self.letter_points,
                                               "".join(removed_letters))

            player.add_points(points)

            log_action("Player {} played '{}' for {} points"
                       .format(player.get_name(), best_word, points))
            self.current_player_pick_letters()
            self.next_player()

        log_action("===\n{} tiles remaining\n===".format(self.n_tiles))

        self.end_game()

def log_action(message):
        print(message)
