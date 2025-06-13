from collections import deque

from card import Card
from card_pile import CardPile
from column import Column

class Table:
    column_count = 7
    cards_required = int((column_count + 1) / 2 * column_count)

    def __init__(self, cards: deque[Card]):
        card_pile = CardPile(cards)
        self.columns = [Column(card_pile.take_cards(_ + 1)) for _ in range(Table.column_count)]
        
    def put_cards_to_column(self, cards: deque[Card], col: int) -> None:
        if col not in range(1, self.column_count + 1):
            raise ValueError(f"There is no such column: {col}")
        self.columns[col - 1].put_cards(cards)
        
    def take_cards_from_column(self, num:int, col: int) -> deque[Card]:
        if col not in range(1, self.column_count + 1):
            raise ValueError(f"There is no such column: {col}")
        cards = self.columns[col - 1].take_cards(num)
        return cards
     
    
    def draw(self, col: int, row: int) -> None:
        pos = col
        for column in self.columns: 
            column.draw(pos, row)
            pos += 6
    