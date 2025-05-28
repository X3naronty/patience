import random
from collections import deque

from card import Card
from card_pile import CardPile


class ReservePile:
    def __init__(self, cards: deque[Card], mode: str):
        self._closed_cards = CardPile(cards)
        self._opened_cards = CardPile() 
        
        if mode != 'hard' and mode != 'light':
            raise ValueError("Nie ma takiego poziomu trudności")
        self.cards_visible = 3 if mode == 'hard' else 1
        
    def take_card(self) -> Card:
        card , = self._opened_cards.take_cards(1)
        return card
    
    def reset(self) -> None:
        if self._closed_cards:
            raise ValueError("Wszystkie karty muszą być otwarte")
        
        cards = self._opened_cards.take_cards(len(self._opened_cards))
        for card in cards: 
            card.flip()
        random.shuffle(cards)
        self._closed_cards.put_cards(cards)
    
    def open_cards(self) -> None:
        if not self._closed_cards:
            raise ValueError("Trzeba odnowa przetasować stos reserwowy")
        count = self.cards_visible
        count = min(count, len(self._closed_cards))
        cards = self._closed_cards.take_cards(count)
        for card in cards: 
            card.flip()
        self._opened_cards.put_cards(cards)

    def draw(self, col: int, row: int) -> None:
        self._closed_cards.draw(col, row)

        pos = col + 8
        num = min(self.cards_visible, len(self._opened_cards)) 
        for i in range(num):
            self._opened_cards.cards[-num + i].draw(pos, row)
            pos += 3


