import os
import sys
import pickle as pkl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimal_policy_training.compute_transition_probabilities import State
from utility_functions.utility_functions import *

MIN_BET = 20

class ValueIteration:
    def __init__(self, player_transitions, dealer_transitions, utility_function, gamma = 1.0):
        self.player_transitions = player_transitions
        self.dealer_transitions = dealer_transitions
        self.gamma = gamma
        self.utility_function = utility_function

    def get_state_actions(self, state):
        if state.is_player_bust():
            return []
        potential_actions = self.player_transitions[state].keys()
        actions = []

        for action in potential_actions:
            if self.player_transitions[state][action] != []:
                actions.append(action)

        return actions  
    

    def is_terminal_state(self, state):
        return self.get_state_actions(state) == [] or state == State(((-1,),(0,)))
    
    def get_reward(self, payoff, initial_bankroll, current_bankroll):
        original_utility = self.utility_function(initial_bankroll, current_bankroll)
        new_utility = self.utility_function(initial_bankroll, current_bankroll + (payoff*MIN_BET))

        return new_utility - original_utility
    
    def process_reward(self, state, initial_bankroll, current_bankroll):
        if state.is_player_bust():
            return self.get_reward(-1, initial_bankroll, current_bankroll)
        
        if state.is_dealer_bust():
            return self.get_reward(1, initial_bankroll, current_bankroll)
        
        if state.player_has_blackjack() and state.dealer_has_blackjack():
            return self.get_reward(0, initial_bankroll, current_bankroll)
        
        if state.player_has_blackjack():
            return self.get_reward(1, initial_bankroll, current_bankroll)
        
        if state.dealer_has_blackjack():
            return self.get_reward(-1, initial_bankroll, current_bankroll)
        
        player_score = state.get_player_value()
        dealer_score = state.get_dealer_value()

        if player_score > dealer_score:
            return self.get_reward(1, initial_bankroll, current_bankroll)
        
        elif player_score < dealer_score:
            return self.get_reward(-1, initial_bankroll, current_bankroll)
        
        else:
            return self.get_reward(0, initial_bankroll, current_bankroll)

    def decide_best_action(self, card_state, initial_bankroll, current_banrkoll):

        actions = self.get_state_actions(card_state)

        if self.is_terminal_state(card_state) or actions == [0]:
            #print('stuck in terminal')
            return 0
        
        else:
            action_values = {
                action: self.evaluate_action(card_state, action, initial_bankroll, current_banrkoll) for action in actions
            }

        #print(action_values)
        return max(action_values, key=action_values.get)
    

    def evaluate_dealer_state(self, state, initial_bankroll, current_bankroll):

        if state not in self.dealer_transitions:
            return 0.0
        
        if state.is_dealer_bust():
            return self.process_reward(state, initial_bankroll, current_bankroll)
        
        dealer_transitions = self.dealer_transitions[state]
        dealer_value = 0.0

        if dealer_transitions == []:
            return self.process_reward(state, initial_bankroll, current_bankroll)
            
        for next_state, prob in dealer_transitions:
            if next_state.is_dealer_bust():
                reward = self.process_reward(next_state, initial_bankroll, current_bankroll)
                dealer_value += prob * reward
            else:
                dealer_value += prob * self.evaluate_dealer_state(next_state, initial_bankroll, current_bankroll)
        return dealer_value
            


    def evaluate_action(self, state, action, initial_bankroll, current_bankroll, gamma = 1.0):
        action_value = 0.0

        if action == 1:
            hit_states = self.player_transitions[state][1]
            action_value = 0.0

            for next_state, prob in hit_states:
                if next_state.is_player_bust():
                    reward = self.process_reward(next_state, initial_bankroll, current_bankroll)
                    action_value += prob * reward
                else:
                    action_value += prob * max(
                        self.evaluate_action(next_state, 1, initial_bankroll, current_bankroll, gamma),
                        self.evaluate_action(next_state, 0, initial_bankroll, current_bankroll, gamma)
                        )
                    
            return gamma * action_value
        
        else:
            stand_states = self.player_transitions[state][0]
            action_value = 0.0
            
            for dealer_start_state, prob in stand_states:
                dealer_value = self.evaluate_dealer_state(dealer_start_state, initial_bankroll, current_bankroll)
                action_value += prob * dealer_value

            return gamma * action_value

# with open('optimal_policy_training/player_transitions.pkl','rb') as pklfile: 
#     player_transitions = pkl.load(pklfile)

# with open('optimal_policy_training/dealer_transitions.pkl', 'rb') as file:
#     dealer_transitions = pkl.load(file)

# state = State(((5,7), (2,)))
# value_iteration = ValueIteration(player_transitions, dealer_transitions, linear_utility)
# print(value_iteration.decide_best_action(state, 100, 100))