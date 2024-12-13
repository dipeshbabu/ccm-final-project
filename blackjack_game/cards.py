'''
This module defines classes to represent a standard deck of playing cards, hands in a card game, and the deck itself. It includes functionality for card ranking, scoring, and deck management to facilitate the desired implementation of Blackjack.
'''

import random

class Card:
    '''
    This class represents a standard playing card with a rank and suit. It includes functionality for getting the value of the card, checking if the card is an ace, and printing the card.    
    '''
    def  __init__(self, rank, suit):
        '''
        Initializes a card with a rank and suit.

        Inputs:
            - rank (str): The rank of the card, from 2 to 10, J, Q, K, A.
            - suit (str): The suit of the card, from Hearts, Diamonds, Clubs, Spades
        '''
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        '''
        Returns a string representation of the card, used for debugging.
        '''
        return f"{self.rank} of {self.suit}"
    
    def __str__(self):
        '''
        Returns a general string representation of the card.
        '''
        return f'{self.rank} of {self.suit}'
    
    def get_value(self):
        '''
        Returns the value of the card based on its rank. Ace is defaulted to 11, but may be adjust in other parts of the code.
        '''
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
        

        
    def is_ace(self):
        '''
        Returns True if the card is an ace, False otherwise.
        '''
        return self.rank == 'A'
    
class Hand:
    '''
    This class represents a hand in a card game. It includes functionality for initializing a hand, updating the score of a hand, hitting a hand with a card, and printing the hand. Used by Player and Dealer classes for managing hands.
    '''
    def __init__(self):
        '''
        Initializes a hand with an empty list of cards, a score of 0, and number of aces in the hand.
        '''
        self.hand = []
        self.num_aces = 0
        self.score = 0

    def initialize_hand(self, card1, *args):
        '''
        Initializes a hand with a list of cards and calculates the score of the hand.

        Inputs:
            - card1 (Card): The first card in the hand.
            - *args (Card): The rest of the cards in the hand.
        '''

        # the hand is updated as a list of cards
        self.hand = [card1] + list(args)
        # the score is calculated as the sum of the values of the cards in the hand
        self.score = sum([card.get_value() for card in self.hand])

        # the number of aces in the hand is calculated
        for card in self.hand:
            if card.is_ace():
                self.num_aces += 1

        # if the score is greater than 21 and there are aces in the hand, the score is adjusted by subtracting 10 for each ace until the score is less than or equal to 21. This essentially handles player/dealer choice of ace value.
        if self.score > 21 and self.num_aces > 0:
            # changing ace to 1 implicitly
            self.score -= 10
            # decrementing the number of aces after changing the value of an ace
            self.num_aces -= 1

    def __str__(self):
        '''
        String representation of the hand.
        '''
        return ', '.join(str(card) for card in self.hand)
        
    def reset_hand(self):
        '''
        Resets the hand to an empty list of cards, 0 aces, and a score of 0.
        '''
        self.hand = []
        self.num_aces = 0
        self.score = 0
    
    def update_score(self, card):
        '''
        Adds the value of a new card to the score of the hand.

        Inputs:
            - card (Card): The card to be added to the hand
        
        Outputs:
            - score (int): The updated score of the hand. (Returns -1 if bust)
        '''
        if card.is_ace():
            # incrementing the number of aces in the hand
            self.num_aces += 1
        # the value of the card is added to the score
        card_value = card.get_value()

        # managing the value of aces in the hand if available if the score exceeds 21
        if self.score + card_value > 21 and self.num_aces > 0:
            # changing ace to 1 implicitly
            self.score -= 10
            # decrementing the number of aces after changing the value of an ace
            self.num_aces -= 1
            # updating the score with the new card value
            self.score += card_value
        else:
            # updating the score with the new card value
            self.score += card_value
    
    def hit(self, card):
        '''
        Manages the hit action for a hand. Adds a card to the hand, updates the score, and returns the score of the hand.

        Inputs:
            - card (Card): The card to be added to the hand
        
        Outputs:
            - score (int): The updated score of the hand. (Returns -1 if bust)
        '''
        # adding the card to the hand
        self.hand.append(card)
        # updating the score of the hand
        self.update_score(card)
        return self.score

    def get_score(self):
        '''
        Returns the score of the hand. Returns -1 if the score is greater than 21 (bust).
        '''
        return -1 if self.score > 21 else self.score
    
    def print_hand(self):
        '''
        Prints the hand of cards.
        '''
        print(str(self))

    def __str__(self):
        '''
        String representation of the hand.
        '''
        return ', '.join(str(card) for card in self.hand)
    
    def has_blackjack(self):
        '''
        Returns True if the hand is a blackjack (score of 21 with 2 cards), False otherwise.
        '''
        return self.score == 21 and len(self.hand) == 2
    
    def bust(self):
        '''
        Returns True if the hand is a bust (score greater than 21), False otherwise.
        '''
        return self.score > 21
    
    def get_hand(self):
        '''
        Returns the list of cards in the hand.
        '''
        return self.hand
    
    def get_hand_ranks(self):
        '''
        Gets the ranks of the cards in the hand.
        '''
        # uses the get_value method of the Card class
        card_ranks = [card.get_value() for card in self.hand]
        return card_ranks

class Deck:
    '''
    This class represents a deck of playing cards. It includes functionality for creating a deck, shuffling the deck, and dealing a card from the deck.
    '''
    def __init__(self, num_decks):
        '''
        Initializes a deck with a specified number of decks, and creates and shuffles the deck.
        '''
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.num_decks = num_decks
        # creates a deck with the specified number
        self.cards = self.create_deck()
        # shuffles the deck
        self.shuffle()

    def create_deck(self):
        '''
        Creates a deck of cards with the specified number of decks.
        '''
        # returning a list of cards with all possible combinations of ranks and suits
        return [Card(rank, suit) for rank in self.ranks for suit in self.suits] * self.num_decks
    
    def shuffle(self):
        '''
        Shuffles the deck
        '''
        random.shuffle(self.cards)

    def deal(self):
        '''
        Deals the top card from the deck. Since the deck is shuffled this is a random card.
        '''
        return self.cards.pop()