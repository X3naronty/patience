import time
from card import Card
import random
from collections import deque

class CardDeck:
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = deque([Card(rank, suit) for rank in CardDeck.ranks for suit in CardDeck.suits])
        random.shuffle(self.cards)

        

                
    
# a = CardDeck()
# for i in range(len(a.cards)):
#     card, = a.take_cards(1)
#     print(card.rank + ' ' + card.suit)
    
