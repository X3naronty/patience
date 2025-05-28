from collections import deque

from card import Card
from card_pile import CardPile


class EndPilesArea:
    def __init__(self):
        self.piles = [
            CardPile(),
            CardPile(),
            CardPile(),
            CardPile(),
        ]
    
    def get_card_count(self) -> int:
        number = 0
        for pile in self.piles:
            number += len(pile)
        
        return number
        
    def draw(self, col: int, row: int) -> None:
        pos = col
        for pile in self.piles:
            pile.draw(pos, row)
            pos += 6

    def put_card(self, card: Card) -> None:
        for pile in self.piles:
            if not pile:
                # one of the end piles is empty
                if card.rank_num == 0:     
                    pile.put_cards(deque([card]))
                    return
            elif pile[-1].rank_num + 1 == card.rank_num and pile[-1].suit == card.suit:
                # one of the end piles is not empty 
                # and you can put card accoring to rules
                pile.put_cards(deque([card]))
                return
       
        raise ValueError("You can't add this card to the end stack")
