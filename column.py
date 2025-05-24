from collections import deque
from card import Card
from playing_area import PlayingArea

class Column(PlayingArea):
    def __init__(self, cards: deque[Card]):
        self.cards = cards
        self.cards[-1].flip()
        
        