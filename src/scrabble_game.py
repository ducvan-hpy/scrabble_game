#! /usr/bin/env python3

from datetime import datetime
import scrabble_lib
import time
import unidecode


N_PLAYERS = 2
# Point to add to your total if play all your tiles
SCRABBLE_POINTS = 50


class Player:
    def  __init__(self, name, logfile):
        self._name = name
        self._letters = []
        self._points = 0
        self._logfile = logfile

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
                log_action(self._logfile, "Player {} used blank tile to "
                           "replace '{}'".format(self.get_name(), l))

        return removed_letters

    def add_points(self, points):
        self._points += points


class Game:
    def __init__(self, dictionary_file, distribution_file):
        # Format log file name: "game_YYYY_MM_DD_hh_mm_ss.log"
        dt = datetime.now()
        self.logfile = dt.strftime("game_%Y%m%d_%H%M%S.log")
        print("Game logs will be saved in {}".format(self.logfile))

        self.letter_set, self.letter_points = \
            scrabble_lib.load_distribution_file(distribution_file)
        self.n_tiles = sum(self.letter_set.values())
        self.word_map = scrabble_lib.load_dictionary_file(dictionary_file)

        log_action(self.logfile,
                   "Start game with {} tiles\n===".format(self.n_tiles))

        # Named player "1", "2", "3"...
        self.players = [Player(i + 1, self.logfile) for i in range(N_PLAYERS)]
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

    def add_letters_to_set(self, letters):
        for l in letters:
            self.letter_set[l] += 1
            self.n_tiles += 1

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
            log_action(self.logfile, "Player {} has picked a '{}' tile".
                       format(player.get_name(), l))

        return l

    def current_player_pick_letters(self):
        player = self.current_player()
        n_letters = scrabble_lib.SET_SIZE - player.get_number_letters()
        letters = scrabble_lib.generate_random_input(self.letter_set, n_letters)
        self.remove_letters_from_set(letters)
        player.add_letters(letters)
        log_action(self.logfile,
                   "Player {} has picked {}".format(player.get_name(), letters))


    def current_player_substitute_letters(self):
        '''
        If a player cannot play, he can substitute some letters from his hand
        to the tiles bag.
        We will simplify this case and swap all the letters in his hand.
        '''
        player = self.current_player()
        letters = scrabble_lib.generate_random_input(self.letter_set,
                                                     scrabble_lib.SET_SIZE)
        old_letters = player.get_letters()

        log_action(self.logfile,"Player {} has swapped {} for {}".format(
            player.get_name(), old_letters, letters))

        self.remove_letters_from_set(letters)
        self.add_letters_to_set(old_letters)

        player.add_letters(letters)
        player.remove_letters(old_letters)

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
        log_action(self.logfile,
                   "Player {} has the tile closest to 'A', he will be the "
                   "first player to play\n===".format(player.get_name()))

        for _ in range(N_PLAYERS):
            self.current_player_pick_letters()
            self.next_player()

    def current_player_play(self):
        '''
        Play 1 turn with current player.
        Return True if he can play, False otherwise.
        '''
        player = self.current_player()
        log_action(self.logfile, "--\nPlayer {} hand: {}"
                   .format(player.get_name(), player.get_letters()))

        # Because of blank tiles, we will recompute the points
        best_word, _ = scrabble_lib.find_best(self.letter_points, self.word_map,
                                              player.get_letters())

        if best_word:
            removed_letters = player.remove_letters(best_word)
            points = scrabble_lib.count_points(self.letter_points,
                                               "".join(removed_letters))

            player.add_points(points)

            log_action(self.logfile, "Player {} played '{}' for {} points"
                       .format(player.get_name(), best_word, points))

            if len(best_word) == scrabble_lib.SET_SIZE:
                player.add_points(SCRABBLE_POINTS)
                log_action(self.logfile,
                           "Player {} played {} tiles and got {} extra points"
                           .format(player.get_name(), len(best_word),
                                   SCRABBLE_POINTS))

            if not self.is_over():
                self.current_player_pick_letters()
            return True
        else:
            log_action(self.logfile,
                       "Player {} cannot play".format(player.get_name()))
            return False

    def end_game(self):
        can_play = True
        while can_play:
            can_play = False
            for _ in range(N_PLAYERS):
                if self.current_player_play():
                    can_play = True
                self.next_player()

        log_action(self.logfile, "===")

        for _ in range(N_PLAYERS):
            player = self.current_player()
            log_action(self.logfile, "Player {} hand: {}"
                       .format(player.get_name(), player.get_letters()))

            log_action(self.logfile, "Player {} got {} points"
                       .format(player.get_name(), player.get_points()))
            self.next_player()

    def play(self):
        self.setup_game()

        while not self.is_over():
            if not self.current_player_play() and \
               self.n_tiles >= scrabble_lib.SET_SIZE:
                # If current player can not play and there is enough tiles
                #  to draw a new hand
                self.current_player_substitute_letters()
            self.next_player()

        log_action(self.logfile,
                   "===\n{} tiles remaining. Finishing the game with tiles "
                   "in players hands.".format(self.n_tiles))

        self.end_game()

def log_action(filename, message):
    with open(filename, "a") as f:
        f.write(message + "\n")
