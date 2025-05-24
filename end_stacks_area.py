from playing_area import PlayingArea
from card import Card
from collections import deque

class EndStacksArea(PlayingArea):
    def __init__(self):
        self.stacks = [
            deque([]),
            deque([]),
            deque([]),
            deque([])
        ]
        
    def draw(self) -> None:
        pos = 30
        for stack in self.stacks:
            EndStacksArea.draw_card_field(pos, 1)
            if stack:
                stack[-1].draw(pos, 1)
            pos += 6
    
    def add_card(self, card: Card):
       pass 

if __name__ == "__main__":
    a = EndStacksArea()
    a.stacks[0].append(Card('Ace', 'spades'))
    a.stacks[0][0].flip()
    a.draw()