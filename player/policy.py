'''
This file contains the PlayerPolicy class which is used to make decisions for the player in the blackjack game.
'''

import os
import sys
import pickle as pkl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utility_functions.utility_functions import *
from optimal_policy_training.value_iteration import ValueIteration
from optimal_policy_training.compute_transition_probabilities import State

class PlayerPolicy():
    '''
    This class is used to make decisions for the player in the blackjack game. Takes in the current bankroll, initial bankroll,
    minimum bet, player transitions, dealer transitions, and utility function as input.
    '''
    def __init__(self,current_bankroll, initial_bankroll, min_bet, player_transitions, dealer_transitions , utility_function = linear_utility):
        '''
        Player Policy is initialized with the current bankroll, initial bankroll, minimum bet, player transitions, dealer transitions, 
        and utility function. The value iteration object is also initialized.
        '''
        # storing the current bankroll, initial bankroll, minimum bet, and utility function      
        self.current_bankroll = current_bankroll
        self.initial_bankroll = initial_bankroll
        self.min_bet = min_bet
        self.utility_function = utility_function
        # storing the player transitions and dealer transitions
        self.player_transitions = player_transitions
        self.dealer_transitions = dealer_transitions

        # initializing the value iteration object based on the player transitions, dealer transitions, and utility function
        self.value_iteration = ValueIteration(self.player_transitions, self.dealer_transitions, linear_utility)


    def make_decision(self,state):
        '''
        Makes a decision for the player based on the current state. The decision is made using the value iteration object.
        '''
        # getting the best action based on the current state from the value iteration object
        best_action = self.value_iteration.decide_best_action(state, self.initial_bankroll, self.current_bankroll)

        # returning the decision based on the best action
        if best_action == 1:
            return "hit"
        else:
            return "stand"

