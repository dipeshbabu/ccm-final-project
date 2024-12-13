'''
This script defines the Player class for the Blackjack game.
'''


import sys
import os
from player.policy import PlayerPolicy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackjack_game.cards import Hand, Card
from optimal_policy_training.compute_transition_probabilities import State


class Player:
    '''
    Class to represent a player in the Blackjack game
    Methods:
        - __init__: initializes the player with a current bankroll, initial bankroll, minimum bet and player policy
        - initialize_hand: initializes the player's hand with two cards
        - reset_hand: resets the player's hand
        - hit: adds a card to the player's hand
        - stand: player stands
        - make_decision: makes a decision based on the current state
        - get_score: gets the score of the player's hand
        - print_hand: prints the player's hand
        - current_state: gets the current state of the player
        - has_blackjack: checks if the player has blackjack
        - bust: checks if the player has busted
        - get_hand: gets the player's hand
    '''
    def __init__(self, current_bankroll, initial_bankroll, min_bet, player_policy = None):
        '''
        Initializes the player with a current bankroll, initial bankroll, minimum bet and player policy
        '''

        # Initialize the player with the current bankroll, initial bankroll, minimum bet and player policy
        self.policy = player_policy if player_policy else PlayerPolicy(current_bankroll, initial_bankroll, min_bet)
        # Initialize the player's hand
        self.hand = Hand()
        # Initialize the player's initial bankroll
        self.initial_bankroll = initial_bankroll
        # Initialize the player's current bankroll
        self.bankroll = current_bankroll
        # Initialize the player's minimum bet
        self.min_bet = min_bet

    def initialize_hand(self, card1, card2):
        '''
        Initializes the player's hand with two cards
        '''
        self.hand.initialize_hand(card1, card2)

    def reset_hand(self):
        '''
        Resets the player's hand
        '''
        self.hand.reset_hand()
    
    def hit(self, card):
        '''
        Adds a card to the player's hand and calls the hit method of the hand object
        '''
        self.hand.hit(card)

    def stand(self):
        # player stands
        pass

    def make_decision(self, dealer_card):
        '''
        Returns the decision made by the player based on the current state
        '''
        return self.policy.make_decision(self.current_state(dealer_card))
    
    def get_score(self):
        '''
        Returns the score of the player's hand
        '''
        return self.hand.get_score()
    
    def print_hand(self):
        '''
        Prints the player's hand
        '''
        self.hand.print_hand()

    def current_state(self, dealer_card):
        '''
        Returns the current state of the player
        '''
        # collects player card's rank and dealer card's rank
        player_card_ranks = self.hand.get_hand_ranks()
        dealer_card_rank = dealer_card.get_value()
        # creates a state object with the player card's rank and dealer card's rank
        player_card_rank_tuple = tuple(player_card_ranks)
        # returns the state object
        return State((player_card_rank_tuple,(dealer_card_rank,)))

    def has_blackjack(self):
        '''
        Returns True if the player has blackjack
        '''
        return self.hand.has_blackjack()
    
    def bust(self):
        '''
        Returns True if the player has busted
        '''
        return self.hand.bust()
    
    def get_hand(self):
        '''
        Returns the player's hand
        '''
        return self.hand.get_hand()

    def reset_hand(self):
        '''
        Resets the player's hand
        '''
        self.hand.reset_hand()