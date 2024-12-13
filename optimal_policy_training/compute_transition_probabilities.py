import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackjack_game.dealer import DealerPolicy
from collections import Counter
from globals import *

class State:
    '''
    This class is responsible for managing the state of the game, specifically as it pertains to the bellman equation. It keeps track of the player and dealer cards and their values.
    '''
    def __init__(self, state):
        '''
        Initializes the state with the player and dealer cards and their values.
        '''
        # First element of the state tuple is the player cards
        self.player_cards = list(state[0])
        # Second element of the state tuple is the dealer cards
        self.dealer_cards = list(state[1])
        # Arrange the cards
        self.order_cards()
        # Get the player value
        self.player_value = self.get_player_value()
        # Get the dealer value
        self.dealer_value = self.get_dealer_value()

    def order_cards(self):
        '''
        Arranges the cards in ascending order.
        '''
        # Sort the player cards
        self.player_cards = sorted(self.player_cards)
        # Sort the dealer cards
        self.dealer_cards = sorted(self.dealer_cards)

    def get_cards(self):
        '''
        Gets all the cards in the state.
        '''
        return self.player_cards + self.dealer_cards
    
    def get_player_cards(self):
        '''
        Gets the player cards.
        '''
        return self.player_cards
    
    def get_dealer_cards(self):
        '''
        Gets the dealer cards.
        '''
        return self.dealer_cards
    
    def is_player_bust(self):
        '''
        Returns true if the state of the player is bust.
        '''
        return self == State(((-1,), (0,)))
    
    def is_dealer_bust(self):
        '''
        Returns true if the state of the dealer is bust.
        '''
        return self.dealer_cards == [-1]
    
    def player_has_blackjack(self):
        '''
        Returns true if the player has blackjack.
        '''
        return self.player_value == 21 and len(self.player_cards) == 2
    
    def dealer_has_blackjack(self):
        '''
        Returns true if the dealer has blackjack.
        '''
        return self.dealer_value == 21 and len(self.dealer_cards) == 2
    
    def is_bust(self):
        '''
        Return true if either the player or dealer is bust.
        '''
        return self.is_player_bust() or self.is_dealer_bust()
    
    def valid_draws(self, deck_cards):
        '''
        Returns the valid draws from the deck.
        '''
        # Get the current deck
        current_deck = Counter(deck_cards)
        # Get the current cards
        current_cards = Counter(self.get_cards())
        # Get the remaining cards
        remaining_cards = list((current_deck - current_cards).elements())
        # Return the remaining cards
        return list(set(remaining_cards))


    def get_player_value(self):
        '''
        Returns the value of the player's cards.
        '''
        # Initialize the number of aces
        num_aces = 0
        value = 0
        
        # for card in player cards 
        for card in self.player_cards:
            # if card is 11
            if card == 11:
                # increment the number of aces
                num_aces += 1
            # add the card to the value
            value += card

        # while the value is greater than 21 and the number of aces is greater than 0, decrement the value by 10 and decrement the number of aces
        while value > 21 and num_aces >0:
            # decrease the value of aces from 11 to 1
            value -= 10
            # decrement the number of aces
            num_aces -= 1
        # if the value is greater than 21, set the player cards to -1
        if value > 21:
            # set the player cards to -1 if busted
            self.player_cards = [-1]
            self.dealer_cards = [0]
            self.player_value = -1
            self.dealer_value = 0
        return value
    
    def num_aces(self):
        '''
        Collects the num of aces in the player cards.
        '''
        return self.player_cards.count(11)

    def get_dealer_value(self):
        '''
        Returns the value of the dealer's cards. Adjusts the value of aces if the dealer is bust.
        '''
        # collects the number of aces
        num_aces = 0
        # initializes the value
        value = 0
        # for card in dealer cards
        for card in self.dealer_cards:
            # if card is ace, increment the number of aces
            if card == 11:
                num_aces += 1
            # add the card to the value
            value += card
        
        # if the value is greater than 21 and the number of aces is greater than 0, decrement the value by 10 and decrement the number of aces
        while value > 21 and num_aces > 0:
            # decrease the value of aces from 11 to 1
            value -= 10
            num_aces -= 1
        # if the value is greater than 21, set the dealer cards to -1
        if value > 21:
            # set the dealer cards to -1 if busted
            self.dealer_cards = [-1]
            self.dealer_value = -1
        
        # return the value 
        return value
    

    def get_hit_states(self):
        '''
        Returns the hit states for the player.    
        '''
        # initialize the hit states
        hit_states = []

        # if the player is bust, return an empty list - no hit states
        if self.is_bust():
            return hit_states

        # if the player has blackjack, return an empty list - no further hit states
        if self.player_value == 21:
            return hit_states
        
        else:
            # get the list of cards that can be drawn from the deck
            new_states = [State((self.player_cards + [card], self.dealer_cards)) for card in self.valid_draws(deck_cards)]

            # if all the new states are bust, return no hit states
            if all([state.is_player_bust() for state in new_states]):
                return hit_states
            
            # if any of the new states are bust, add a bust state to the hit states
            if any([state.is_player_bust() for state in new_states]):
                hit_states.append(State(((-1,), (0,))))
            
            # otherwise, add the new states to the hit states
            hit_states += [state for state in new_states if state.player_value <= 21 and not state.is_player_bust()]
                 
        return hit_states
 

    def get_dealer_states(self, dealer_policy):
        '''
        Gets the dealer states based on the dealer policy. I.e, the states of the game after the player has decided to stand.
        '''

        dealer_states = []
        
        # if the player is bust or the player's value is less than 12 and there are no aces, return the dealer states
        if self.is_bust() or ((self.get_player_value() <= 12) and (self.num_aces() == 0)):
            return dealer_states
        
        # if the dealer is hit based on the dealer policy, get the new states based on valid draws from the deck
        if dealer_policy.make_decision(self.dealer_value) == "hit":
            # get the list of cards that can be drawn from the deck
            for card in self.valid_draws(deck_cards):
                # get the new state for each valid draw
                new_state = State((self.player_cards, self.dealer_cards + [card]))

                # if the new state is bust, add the new state to the dealer states -> this would be ((player_hand), (-1,))
                if new_state.is_dealer_bust():
                    if new_state not in dealer_states:
                        dealer_states.append(new_state)

                # if the new state is not bust, add the new state to the dealer states
                if new_state.dealer_value <= 21:
                    dealer_states.append(new_state)

        return dealer_states
    
    def get_card_probs(self, new_card):
        '''
        Gets the probability of drawing a specified new card from the deck.
        '''
        
        # get the current deck and current cards
        current_deck = Counter(deck_cards)
        current_cards = Counter(self.get_cards())
        # get the remaining cards
        remaining_cards = list((current_deck - current_cards).elements())
        # return the probability of drawing the new card from the remaining cards
        return round((remaining_cards.count(new_card) / len(remaining_cards)),3)

    def get_state_prob(self, new_state):
        '''
        Gets the probability of transitioning to a new state from the current state.
        '''
        # get the old cards and new cards
        old_cards = Counter(self.get_cards())
        new_cards = Counter(new_state.get_cards())
        # get the new card
        new_card = list((new_cards - old_cards).elements())[0]
        # return the probability of drawing the new card
        return self.get_card_probs(new_card)
       
    def get_probs(self, input_states):
        '''
        For a given list of states, returns the probabilities of transitioning to each state from the current state.
        '''
        # if the input states are empty, return an empty list
        if input_states == []:
            return []
        
        # initialize the probabilities and states with probabilities
        # probs is used to keep track of the probabilities of transitioning to each state, so that 1 - sum(probs) can be calculated for the bust state
        probs = []
        states_with_probs = []
        # track the index of the bust state, -1 if no bust state
        bust_idx = -1

        # for each state in the input states
        for idx, state in enumerate(input_states):
            # if the player or dealer is bust, set the bust index to the current index
            if state.is_player_bust() or state.is_dealer_bust():
                bust_idx = idx
            else:
                # get the new card
                # get the current state count and new state count
                current_state_count = Counter(self.get_cards())
                new_state_count = Counter(state.get_cards())
                # get the new card probability
                new_card = list((new_state_count - current_state_count).elements())[0]
                # get the probability of drawing the new card
                prob = self.get_card_probs(new_card)
                # add the probability to the list of probabilities
                probs.append(prob)
                
                # add the state and probability to the list of states with probabilities
                states_with_probs.append((state, prob))

        # if there is a valid bust states
        if bust_idx != -1:
            # calculate the total probability of transitioning to the bust state
            total_prob = 1.0 - sum(probs)
            # add the bust state and total probability to the list of states with probabilities
            states_with_probs.append((input_states[bust_idx], total_prob))

        # return the states with probabilities
        return states_with_probs

    def __eq__(self, other):
        '''
        Returns true if the player cards and dealer cards are the same for two state objects
        '''
        # return true if the player cards and dealer cards are the same
        return self.player_cards == other.player_cards and self.dealer_cards == other.dealer_cards
    
    def __repr__(self):
        '''
        Return the player and dealer cards for the state as a string
        '''
        return f"Player: {self.player_cards}, Dealer: {self.dealer_cards}"
    
    def __hash__(self):
        '''
        Returns a hash of the player and dealer cards. Used for a dictionary key.
        '''
        return hash((tuple(self.player_cards), tuple(self.dealer_cards)))


def get_starting_states(deck_cards):
    '''
    Get the starting states for the game. The starting states are the states of the game when the player has two cards and the dealer has one card.
    '''
    # initialize the starting states with the bust state for the player
    starting_states = [State(((-1,),(0,)))]

    # get the unique cards in the deck
    unique_cards = list(set(deck_cards))

    # for each combination of player cards
    for player_card1 in unique_cards:
        # for each combination of player cards
        for player_card2 in unique_cards:
            # we add the bust state for the dealer with the current player hand
            bust_state = State(((player_card1, player_card2), (-1,)))
            if bust_state not in starting_states:
                # add the bust state to the starting states
                starting_states.append(bust_state)
            
            # for all possible dealer cards
            for dealer_card in range(2,12):
                # computes the starting state with the given player and dealer cards
                new_state = State(((player_card1, player_card2), (dealer_card,)))
                if new_state not in starting_states:
                    # add the new state to the starting states
                    starting_states.append(new_state)

    return starting_states


# starting_states = get_starting_states(deck_cards)

# initialize the player and dealer dictionaries
player_dict = {}
dealer_dict = {}
# dealer_policy = DealerPolicy()

def build_transition_dict(starting_states, player_turn = True):
    '''
    Builds the dictionary of transition probabilities for the player and dealer states. Uses recursion to build the dictionary for all possible substages of the game from the starting states.
    '''
    # if it is the player's turn, we initialize the states not in the player dictionary with the starting states
    states_not_in_dict = []
    if player_turn:
        # if the player dictionary is empty, we initialize the states not in the player dictionary with the starting states
        if player_dict.keys():
            states_not_in_dict = [state for state in starting_states]
        else:
            # if the player dictionary is not empty, we initialize the states not in the player dictionary with the starting states that are not in the player dictionary
            states_not_in_dict = starting_states
        if not states_not_in_dict:
            return
        
    else:
        # if it is the dealer's turn, we initialize the states not in the dealer dictionary with the starting states that are not in the dealer dictionary
        states_not_in_dict = [state for state in starting_states if state not in dealer_dict]
        if not states_not_in_dict:
            return
    
    # for each state not already in the dictionary
    for state in states_not_in_dict:
        if player_turn:
            # if it is the player's turn, we initialize the hit and stand states for the player
            hit_states = state.get_hit_states()
            stand_states = state.get_dealer_states(DealerPolicy())
            # we add the hit and stand states to the player dictionary
            player_dict[state] = {
                1: state.get_probs(hit_states),
                0: state.get_probs(stand_states)
            }
            # we then build the transition dictionary for the hit and stand states (and every subsequent substages of the game) for the player
            build_transition_dict(hit_states)
            build_transition_dict(stand_states, player_turn = False)

        else:
            # if it is the dealer's turn, we initialize the dealer states for the dealer
            dealer_states = state.get_dealer_states(DealerPolicy())
            dealer_dict[state] = state.get_probs(dealer_states)

            # we then build the transition dictionary for the dealer states (and every subsequent substages of the game) for the dealer
            build_transition_dict(dealer_states, player_turn = False)