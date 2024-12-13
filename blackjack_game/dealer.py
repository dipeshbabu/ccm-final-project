'''
This module contains the Dealer class and DealerPolicy class. The Dealer class is responsible for managing the dealer's hand, making decisions based on the dealer's policy, and calculating the dealer's score. The DealerPolicy class is responsible for defining the dealer's policy for hitting or standing based on the dealer's score - it is a fixed strategy based on casino rules.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackjack_game.cards import Hand

class Dealer:
    '''
    This class represents the dealer in a blackjack game. It includes functionality for managing the dealer's hand, making decisions based on the dealer's policy, and calculating the dealer's score.
    '''
    def __init__(self, dealer_policy = None):
        '''
        Initializes the dealer with a dealer policy and an empty hand.
        '''
        self.policy = dealer_policy if dealer_policy else DealerPolicy()
        self.hand = Hand()

    def initialize_hand(self, card1):
        '''
        Initializes the dealer's hand with a single card (equivalent to one hidden)
        '''
        self.hand.initialize_hand(card1)

    def reset_hand(self):
        '''
        Resets the dealer's hand
        '''
        self.hand.reset_hand()

    def calculate_score(self):
        '''
        Calculates the score of the dealer's hand.
        '''
        self.hand.calculate_score()
    
    def hit(self, card):
        '''
        Makes the dealer hit with a card.
        '''
        self.hand.hit(card)

    def stand(self):
        pass

    def make_decision(self):
        '''
        Makes a decision based on the dealer's policy.
        '''
        return self.policy.make_decision(self.hand.get_score())
    
    def get_score(self):
        '''
        Gets score of the dealer's hand.
        '''
        return self.hand.get_score()
    
    def print_hand(self):
        '''
        Prints the dealer's hand.
        '''
        self.hand.print_hand()
    
    def has_blackjack(self):
        '''
        Returns True if the dealer has blackjack, False otherwise.
        '''
        return self.hand.has_blackjack()
    
    def bust(self):
        '''
        Returns True if the dealer has busted, False otherwise.
        '''
        return self.hand.bust()
    
    def get_hand(self):
        '''
        Returns the list of cards in the dealer's hand.
        '''
        return self.hand.get_hand()
    
    def reset_hand(self):
        '''
        Resets the dealer's hand.
        '''
        self.hand.reset_hand()



class DealerPolicy:
    def make_decision(self, score):
        '''
        Makes a decision based on the dealer's policy.
        '''
        if score < 17:
            # if dealer's score is less than 17, hit
            return "hit"
        else:
            # otherwise, dealer's stand
            return "stand"