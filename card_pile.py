from collections import deque

from card import Card


class CardPile: 
    _field_style = '\u001b[38;2;255;255;255m'
    _reset = '\u001b[0m'
    _field_icon = (
        '🭽▔▔🭾',
        '▏  ▕',
        '🭼▁▁🭿'
    )
    bg = '\u001b[48;2;0;105;0m'  # green background

    def __init__(self, cards: deque[Card] = None):
        if cards is None: 
            self.cards = deque([])
        else: 
            self.cards = cards

    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]
    
    def __bool__(self):
        return bool(self.cards)

    def draw_card_field(self, col: int, row: int) -> None:
        field_icon = CardPile._field_icon
        field_icon_style = CardPile._field_style + CardPile.bg
        reset = CardPile._reset
        for i, r in enumerate(field_icon):
            position = f'\u001b[{i+row};{col}H'
            print(
                f'{position}' +
                f'{field_icon_style}' +
                f'{r}' +
                f'{reset}'
            )

    def take_cards(self, num: int) -> deque[Card]:
        if len(self.cards) < num:
            raise ValueError("There are not enough cards in the pile")
        cards = deque([])
        for i in range(num):
            cards.append(self.cards.pop())
        
        return cards
    
    def put_cards(self, cards: deque[Card]) -> None:
        self.cards.extend(cards)
        
    def draw(self, col: int, row: int):
        if self.cards:
            self.cards[-1].draw(col, row)
        else:
            self.draw_card_field(col, row)
