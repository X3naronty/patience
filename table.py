from collections import deque
from card import Card
from column import Column

class Table:
    column_count = 7
    def __init__(self, game, cards: deque[Card]):
        self.columns = [Column(game.take_cards(cards, _ + 1)) for _ in range(Table.column_count)]