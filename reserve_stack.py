from collections import deque
from card import Card
from playing_area import PlayingArea

class ReserveStack(PlayingArea):
    def __init__(self, cards: deque[Card], mode: str):
        self._closed_cards = cards
        self._opened_cards = deque([]) 
        self.cards_visible = 3 if mode == 'hard' else 1
        
    def take_card(self) -> Card:
        card = self._opened_cards.pop()
        return card
    
    def open_cards(self) -> None:
        for i in range(min(self.cards_visible, len(self._closed_cards))):
            card = self._closed_cards.pop()
            card.flip()
            self._opened_cards.append(card)

    def draw(self) -> None:
        ReserveStack.draw_card_field(1, 1)
        ReserveStack.draw_card_field(8, 1)
        if self._closed_cards:
            self._closed_cards[-1].draw(1, 1)
        
        pos = 8
        num = min(self.cards_visible, len(self._opened_cards)) 
        for i in range(num):
            self._opened_cards[-num + i].draw(pos, 1)
            pos += 3



if __name__ == "__main__":
    a = ReserveStack(
        deque([
            Card('Ace', 'spades'),
            Card('Ace', 'clubs'),
            Card('Ace', 'heartes'),
            Card('Ace', 'diamonds')
        ]),
        "hard"
    )
    a.open_cards()
    # a.open_cards()
    # a.open_cards()
    # a.open_cards()
    a.draw()
            
            