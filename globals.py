# global variables
from collections import Counter

NUM_DECKS = 1
MIN_BET = 20
INITIAL_BANKROLL = 500
NUM_ROUNDS = 15
CARDS = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

FULL_DECK = CARDS * 4 * NUM_DECKS
CARD_COUNTS = Counter(FULL_DECK)
NUM_ITERATIONS = 300

deck_cards = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4 * NUM_DECKS