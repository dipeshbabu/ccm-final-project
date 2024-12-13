

import os
import sys
import json
import pickle as pkl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from player.player import Player, PlayerPolicy
from blackjack_game.dealer import Dealer
from blackjack_game.game import BlackjackGame
from utility_functions.utility_functions import *
from optimal_policy_training.compute_transition_probabilities import State
from blackjack_game.cards import *
from globals import *

current_banks = [420,440,460,480,500,520,540,560,580]

def generate_best_actions_game(player, dealer, bankroll, num_decks = NUM_DECKS, bet = MIN_BET):
    blackjack_game = BlackjackGame(player, dealer, num_decks = num_decks, bet = bet, bankroll = bankroll)
    action = blackjack_game.play_game(actions_return= True)
    return action

def generate_best_actions_per_bankroll_per_function(player, dealer, bankroll, num_decks = NUM_DECKS, bet = MIN_BET, num_games = 50):
    actions = []
    for _ in range(num_games):
        action = generate_best_actions_game(player, dealer, bankroll, num_decks = num_decks, bet = bet)
        for a in action:
            actions.append(a)
    return actions


def save_file(actions, function_name):
    with open(f'action_probs/best_actions_{function_name}.json','w') as file:
        json.dump(actions, file)

def run_best_actions(current_banks, utility_functions, player_transitions_file ='optimal_policy_training/player_transitions.pkl', dealer_transitions_file = 'optimal_policy_training/dealer_transitions.pkl', num_decks = NUM_DECKS, bet = MIN_BET, initial_bankroll = INITIAL_BANKROLL, num_games = 50):

    player_transition_file = player_transitions_file
    dealer_transition_file = dealer_transitions_file

    with open(player_transition_file,'rb') as pklfile: 
        player_transitions = pkl.load(pklfile)

    with open(dealer_transition_file, 'rb') as file:
        dealer_transitions = pkl.load(file)

    values_final_dict = {}

    for function in utility_functions:
        for bank in current_banks:
            player_policy = PlayerPolicy(bank, initial_bankroll, bet, player_transitions, dealer_transitions, function)
            player = Player(bank, initial_bankroll, bet, player_policy)
            dealer = Dealer()
            actions = generate_best_actions_per_bankroll_per_function(player, dealer, bank, num_decks = num_decks, bet = bet, num_games = num_games)
            #print(f'actions = {actions}')
            values_final_dict[bank] = actions
        save_file(values_final_dict, get_utility_function_str(function))
            

run_best_actions(current_banks, [logarithmic_utility], num_games = 25)
# linear_utility, quadratic_utility, quartic_utility, exponential_utility, logarithmic_utility


# current_banks = [400,420,440,460,480,500,520,540,560,580, 600]

# utility_functions = [linear_utility]
# player_policy = PlayerPolicy(500,INITIAL_BANKROLL, MIN_BET, player_transitions, dealer_transitions, utility_functions[0])

# player = Player(500, INITIAL_BANKROLL, MIN_BET, player_policy)
# dealer = Dealer()

# actions = []
# for _ in range(10):
#     blackjack_game = BlackjackGame(player, dealer, num_decks = NUM_DECKS, bet = MIN_BET, bankroll = current_banks[0])

#     action = blackjack_game.play_game(actions_return= True)
#     actions.append(action)

# print(actions)