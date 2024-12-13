'''
Script to run simulations for a given utility function and save the final payoffs in a json file
'''

import os
import sys
import pickle as pkl
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from globals import *
from blackjack_game.round import BlackjackRound
from utility_functions.utility_functions import *
from optimal_policy_training.compute_transition_probabilities import State
from blackjack_game.cards import *


def run_simulations(utility_function = linear_utility, initial_bankroll = INITIAL_BANKROLL, min_bet = MIN_BET, num_rounds = NUM_ROUNDS, num_decks = NUM_DECKS, player_transition_file = 'optimal_policy_training/player_transitions.pkl', dealer_transition_file = 'optimal_policy_training/dealer_transitions.pkl', num_iterations = NUM_ITERATIONS):
    '''
    Function to run simulations for a given utility function and save the final payoffs in a json file
    
    Inputs:
        - utility_function: function, utility function to use
        - initial_bankroll: int, initial bankroll for the player
        - min_bet: int, minimum bet for the player
        - num_rounds: int, number of rounds to play
        - num_decks: int, number of decks to use
        - player_transition_file: str, file path to player transitions
        - dealer_transition_file: str, file path to dealer transitions
        - num_iterations: int, number of iterations to run
    
    Outputs:
        - final_payoffs: list, list of final payoffs for each iteration
    '''

    # Load player and dealer transitions
    player_transitions_file = player_transition_file
    dealer_transitions_file = dealer_transition_file
    with open(player_transitions_file,'rb') as pklfile: 
        player_transitions = pkl.load(pklfile)

    with open(dealer_transitions_file, 'rb') as file:
        dealer_transitions = pkl.load(file)

    # Store final payoffs in a list
    final_payoffs = []
    # for each iteration, run a round and store the final payoff
    for i in range(num_iterations):
        # printing the iteration number
        print(f'Running iteration {i+1}')
        # a round is initialized with the player and dealer transitions, utility function, initial bankroll, minimum bet, number of rounds and number of decks using the BlackjackRound class
        round = BlackjackRound(player_transitions=player_transitions, dealer_transitions=dealer_transitions, utility_function = utility_function, initial_bankroll = initial_bankroll, min_bet = min_bet, num_rounds = num_rounds, num_decks = num_decks)
        # the final payoff is calculated by calling the play_round method of the round object
        final_payoff = round.play_round()
        final_payoffs.append(final_payoff)

    # the final payoffs are saved in a json file
    print(final_payoffs)

    # Save final payoffs in a json file
    file_name_to_save = f'simulations/{get_utility_function_str(utility_function)}_{NUM_ROUNDS}_rounds_final_payoffs.json'
    with open(file_name_to_save, 'w') as file:
        json.dump(final_payoffs, file)

    # return the final payoffs
    return final_payoffs


run_simulations(utility_function= quartic_utility)