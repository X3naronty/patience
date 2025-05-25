from card import Card
from collections import deque
from card_pile import CardPile

class EndPilesArea():
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
            pile.draw(pos, 1)
            pos += 6

    def put_card(self, card: Card) -> None:
        for pile in self.piles:
            if not pile:
                if card.rank_num == 0:     
                    pile._put_cards(deque([card]))
                    return
            elif pile[-1].rank_num + 1 == card.rank_num and pile[-1].suit == card.suit:
                pile._put_cards(deque([card]))
                return
       
        raise ValueError("You can't add this card to the end stack")

if __name__ == "__main__":
    a = EndPilesArea()
    card_1 = Card('Ace', 'spades', 0)
    card_2 = Card('2', 'spades', 1)
    card_3 = Card('Ace', 'heartes', 0)
    card_1.flip()
    card_2.flip()
    card_3.flip()

    a.put_card(card_1)
 
    # a.put_card(card_2)
    a.put_card(card_3)
    a.draw()