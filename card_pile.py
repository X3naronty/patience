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

    def __init__(self, cards: deque[Card] = None):
        if cards is None: self._cards = deque([])
        else: 
            self._cards = cards

    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, index):
        return self._cards[index]
    
    def __bool__(self):
        return bool(self._cards)

    def draw_card_field(self, col: int, row: int) -> None:
        field_icon = self._field_icon
        for i, r in enumerate(field_icon):
            print(
                f'\u001b[{i+row};{col}H' +
                f'{self._field_style}' +
                f'{r}' +
                f'{self._reset}'
            )

    def _take_cards(self, num: int) -> deque[Card]:
        if len(self._cards) < num:
            raise ValueError("There are not enough cards in the pile")
        cards = deque([])
        for i in range(num):
            cards.append(self._cards.pop())
        
        return cards
    
    def _put_cards(self, cards: deque[Card]) -> None:
        self._cards.extend(cards)
        
    def draw(self, col: int, row: int):
        if self._cards:
            self._cards[-1].draw(col, row)
        else:
            self.draw_card_field(col, row)
        

if __name__ == '__main__':
    card_1 = Card('Ace', 'clubs', 0)
    card_2 = Card('Ace', 'hearts', 0)

    a = CardPile(
        deque([card_1, card_2])
    )

    b = CardPile(
        deque([
            
        ])
    )

    cards = a._take_cards(2)
    for card in cards:
        print(card.rank, card.suit)
    # print(a._cards)
    # b._put_cards(card)
    # card = a._take_cards(1)
    # b._put_cards(card)
    # a.draw(1, 1)
    # b.draw(6, 1)