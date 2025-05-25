import time
from card import Card
import random
from collections import deque
from card_pile import CardPile

class CardDeck(CardPile):
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['Ace', '⒉', '⒊', '⒋', '⒌', '⒍', '⒎',
             '⒏', '⒐', '⒑', 'Jack', 'Queen', 'King']
    card_count = len(suits) * len(ranks)

    def __init__(self):
        cards = deque([Card(rank, suit, rank_num) for rank_num, rank in enumerate(CardDeck.ranks) for suit in CardDeck.suits])
        super().__init__(cards)
        random.shuffle(self._cards)
        
    def take_cards(self, num: int) -> deque[Card]:
        cards = super()._take_cards(num)
        return cards

        

                
    
# a = CardDeck()
# for i in range(len(a.cards)):
#     card, = a.take_cards(1)
#     print(card.rank + ' ' + card.suit)
    
