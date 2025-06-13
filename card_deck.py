import random
from collections import deque

from card import Card
from card_pile import CardPile


class CardDeck(CardPile):
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['Ace', '⒉', '⒊', '⒋', '⒌', '⒍', '⒎',
             '⒏', '⒐', '⒑', 'Jack', 'Queen', 'King']
    card_count = len(suits) * len(ranks)

    def __init__(self):
        cards = deque([
            Card(rank, suit, rank_num) 
            for rank_num, rank in enumerate(CardDeck.ranks) 
                for suit in CardDeck.suits
        ])
        super().__init__(cards)
        random.shuffle(self.cards)
        
    def take_cards(self, num: int) -> deque[Card]:
        cards = super().take_cards(num)
        return cards

        

                

    
