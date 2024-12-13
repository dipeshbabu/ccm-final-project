'''
This file contains the BlackjackGame class which is responsible for managing the game state and the flow of the game.
The game is played between a player and a dealer. The player is an instance of the Player class and the dealer is an instance of the Dealer class.
The game is played with a deck of cards. The deck is an instance of the Deck class.
'''

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackjack_game.dealer import Dealer
from blackjack_game.cards import Deck, Card
from player.player import Player
from player.policy import PlayerPolicy
from optimal_policy_training.compute_transition_probabilities import State
from globals import *

# NUM_DECKS = 1
# MIN_BET = 20
# INITIAL_BANKROLL = 300

class BlackjackGame:
    '''
    This class is responsible for managing the game state and the flow of the game.
    '''
    def __init__(self, player, dealer, num_decks=NUM_DECKS, bet=MIN_BET, bankroll=INITIAL_BANKROLL):
        '''
        Initializes the game with a player, dealer, number of decks, and bankroll.
        '''
        # Initialize the deck with the number of decks with the Deck class
        self.deck = Deck(num_decks)
        self.bankroll = bankroll
        self.player = player
        self.dealer = dealer
        self.player_hand = None
        self.dealer_hand = None
        self.dealer_score = 0
        self.player_score = 0
        self.bet = bet

    def initialize_cards(self):
        '''
        Cards are dealt to the player and dealer to start the game.
        Player is dealt two cards and the dealer is dealt one card (which is treated as equivalent to the dealer only having one face-up card)
        '''
        # Deal one card to the dealer
        self.dealer_card = self.deck.deal()
        # Initializes the dealer class with the dealer card
        self.dealer.initialize_hand(self.dealer_card)
        # Update the dealer hand
        self.update_dealer_hand()
        # Deal two cards to the player
        self.player.initialize_hand(self.deck.deal(), self.deck.deal())
        # Update the player hand
        self.update_player_hand()

        #print(f'player hand = {self.player_hand}')
        #print(f'dealer hand = {self.dealer_hand}')

    def update_dealer_hand(self):
        '''
        Updating the dealer class with the dealer hand from BlackjackGame class
        '''
        self.dealer_hand = self.dealer.get_hand()

    def update_player_hand(self):
        '''
        Updating the player class with the player hand from BlackjackGame class
        '''
        self.player_hand = self.player.get_hand()

    def player_turn(self):
        '''
        Plays the player's turn. The player is dealt cards until they decide to stand or bust.
        '''
        # player makes a decision based on the dealer's card first
        player_action = self.player.make_decision(self.dealer_card)

        actions = [player_action]

        # player keeps playing if they decide to hit
        while player_action == 'hit':
            # player hits and is dealt a card. Player class's hit method is called
            self.player.hit(self.deck.deal())
            self.update_player_hand()
            # if player busts, the player's turn ends
            if self.player.bust():
                break
            player_action = self.player.make_decision(self.dealer_card)

            actions.append(player_action)
        #print(f'player actions = {actions}')
        # player's score is updated
        self.player_score = self.player.get_score()

        return actions

    def dealer_turn(self):
        '''
        Simulates the dealer's turn. 
        '''
        # dealer makes a decision based on their hand
        dealer_action = self.dealer.make_decision()

        # dealer makes a decision based on their hand
        while dealer_action == 'hit':
            # dealer hits and is dealt a card. Dealer class's hit method is called
            self.dealer.hit(self.deck.deal())
            # dealer's hand is updated
            self.update_dealer_hand()
            # if dealer busts, the dealer's turn ends
            if self.dealer.bust():
                break
            # dealer makes a decision based on their hand
            dealer_action = self.dealer.make_decision()
        # dealer's score is updated
        self.dealer_score = self.dealer.get_score()

    def get_bankroll(self):
        '''
        Get bankroll
        '''
        return self.bankroll

    def determine_winner(self):
        '''
        Determines the winner of the game based on the player and dealer's scores, and blackjack rules
        '''
        if self.player.bust():
            # If player busts, dealer automatically wins
            return 'dealer'
        elif self.dealer.bust():
            # if the player has not busted and the dealer has, the player automatically wins
            return 'player'
        elif self.player.has_blackjack() and self.dealer.has_blackjack():
            # if both the player and dealer have blackjack, it is a push
            return 'push'
        elif self.player.has_blackjack():
            # if only the player has blackjack, the player wins
            return 'player'
        elif self.player.has_blackjack():
            # if only the dealer has blackjack, the dealer wins
            return 'dealer'
        elif self.player.get_score() > self.dealer.get_score():
            # if all the above conditions are not met, the player wins if their score is higher than the dealer's
            return 'player'
        elif self.player.get_score() < self.dealer.get_score():
            # if all the above conditions are not met, the dealer wins if their score is higher than the player's
            return 'dealer'
        else:
            # the reamining case is if the player and dealer have the same score, which is a push
            return 'push'
        

    def player_payout(self, outcome):
        '''
        Given the outcome of the game, the player's bankroll is updated accordingly
        '''
        # if the outcome is player wins, the player's bankroll is increased by the bet amount
        if outcome == 'player':
            self.bankroll += self.bet
        # if the outcome is dealer wins, the player's bankroll is decreased by the bet amount
        elif outcome == 'dealer':
            self.bankroll -= self.bet
        # if the outcome is a push, the player's bankroll remains the same
        else:
            pass

    def reset_hands(self):
        '''
        Resets the player and dealer's hands to start a new game
        '''
        self.player.reset_hand()
        self.dealer.reset_hand()

    def play_game(self, actions_return = False):
        '''
        Plays the game of blackjack. The game consists of the following steps:
        1. Initialize the cards
        2. Player's turn(s)
        3. Dealer's turn(s)
        4. Determine the winner
        5. Player payout
        6. Reset the hands
        '''
        self.initialize_cards()
        player_actions = self.player_score = self.player_turn()
        self.dealer_score = self.dealer_turn()
        outcome = self.determine_winner()
        self.player_payout(outcome)
        self.reset_hands()


        return player_actions



# # Testing the BlackjackGame class

# dealer = Dealer()
# current_bankroll = 100
# initial_bankroll = 300
# min_bet = 20
# player_policy = PlayerPolicy(current_bankroll, initial_bankroll, min_bet)
# player = Player(current_bankroll, initial_bankroll, min_bet, player_policy)
# game = BlackjackGame(player, dealer)
# game.play_game()

