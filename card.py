from collections import deque

class Card:
    def __init__(self, rank: str, suit: str):
        self._suit = suit
        self._rank = rank
        self.is_opened = False
        self._icons = self.get_icons()

    def get_icons(self) -> deque[tuple[str, ...], ...]:
        reset = '\u001b[0m'
        card = ()
        color = '180;0;0' if self._suit == 'heartes' or self._suit == 'diamonds' else '0;0;0'  

        opened_style = f'\u001b[48;2;200;200;200m\u001b[38;2;{color}m'
        opened_card = (
                opened_style + f'🭽{self.rank}{self.suit}🭾' + reset,
                opened_style + '▏  ▕' + reset,
                opened_style + f'🭼{self.rank}{self.suit}🭿' + reset
            )

        closed_style = '\u001b[48;2;42;0;0m\u001b[38;2;130;130;130m'
        closed_card = (
            closed_style + '🭽▔▔🭾' + reset,
            closed_style + '▏  ▕' + reset,
            closed_style + '🭼▁▁🭿' + reset
        )
        return deque([closed_card, opened_card])
 

    def flip(self):
        self.is_opened = not self.is_opened
        self._icons.rotate(-1)
    
    @property 
    def icon(self):
        return self._icons[0]

    @property 
    def rank(self):
        return self._rank[0]
    
    @property
    def suit(self) -> str:
        match self._suit:
            case "spades":
                return "♠"
            case "heartes":
                return "❤"
            case "clubs":
                return "♣"
            case "diamonds":
                return "◆"
            case _:
                return ""
    
    def draw(self, col: int, row: int) -> None:
        for i, r in enumerate(self.icon):
            position = f'\u001b[{row + i};{col}f'
            print(position + r)
        




# cards = [Card() for _ in range(Card.quantity)]
# for card in cards:
#     print((card.rank + ' ' +card.suit).ljust(8))
    
