'''
This module is responsible for managing a round of the game. It contains the BlackjackRound class, which is responsible for managing the flow of the round. The BlackjackRound class initializes the player, dealer, and game state, and plays the game for a set number of rounds are completed or if the player runs out of money.
'''

import os
import sys
import pickle as pkl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from player.player import Player, PlayerPolicy
from blackjack_game.dealer import Dealer
from blackjack_game.game import BlackjackGame
from utility_functions.utility_functions import *
from optimal_policy_training.compute_transition_probabilities import State
from blackjack_game.cards import *
from globals import *

class BlackjackRound:
    '''
    This class is responsible for managing the flow of the round. Simulates num_rounds of the game and keeps track of the player's bankroll.
    '''

    def __init__(self, player_transitions, dealer_transitions, utility_function = linear_utility, initial_bankroll = INITIAL_BANKROLL, min_bet = MIN_BET, num_rounds = NUM_ROUNDS, num_decks = NUM_DECKS, dealer = None):
        '''
        Initializes the round with the player, dealer, and game state.
        '''

        print(f'running {num_rounds} rounds')

        # Initialize the game state with fixed parameters
        self.min_bet = min_bet
        self.num_rounds = num_rounds
        self.initial_bankroll = initial_bankroll
        self.current_bank = initial_bankroll
        self.current_round = 0
        self.utility_function = utility_function
        self.player_transitions = player_transitions
        self.dealer_transitions = dealer_transitions

        # Initialize the player and dealer with the player policy
        self.player_policy = PlayerPolicy(self.current_bank, self.initial_bankroll, self.min_bet, self.player_transitions, self.dealer_transitions,self.utility_function)
        # player is initialized based on player class
        self.player = Player(self.current_bank, self.initial_bankroll, self.min_bet, self.player_policy)
        # dealer is initialized based on dealer class
        self.dealer = dealer if dealer else Dealer()
        # game is initialized based on BlackjackGame class
        self.blackjack_game = BlackjackGame(self.player, self.dealer, num_decks = num_decks, bet = min_bet, bankroll = initial_bankroll)


    def play_round(self):
        '''
        Plays the blackjack round based on the implementation of BlackjackRound class
        '''
        # Play the game for the set number of rounds or until the player runs out of money
        while self.current_round < self.num_rounds and self.current_bank >= self.min_bet:
            # play the game
            self.blackjack_game.play_game()
            # update the bankroll
            self.current_bank = self.blackjack_game.get_bankroll()
            # increment the round
            self.current_round += 1
            # reinitialize the player, dealer, and game state
            self.blackjack_game = BlackjackGame(self.player, self.dealer, num_decks = NUM_DECKS, bet = MIN_BET, bankroll = self.current_bank)

        print(f'Final bankroll after round: {self.current_bank}')
        # return the final bankroll
        return self.current_bank


# # Code to test the round

#player_policy = PlayerPolicy()

# player_transition_file = 'optimal_policy_training/player_transitions.pkl'
# dealer_transition_file = 'optimal_policy_training/dealer_transitions.pkl'
# with open(player_transition_file,'rb') as pklfile: 
#     player_transitions = pkl.load(pklfile)

# with open(dealer_transition_file, 'rb') as file:
#     dealer_transitions = pkl.load(file)
# round = BlackjackRound(player_transitions=player_transitions, dealer_transitions=dealer_transitions)
# round.play_round()
