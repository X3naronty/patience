from collections import deque

from card import Card
from card_pile import CardPile


class Column(CardPile):
    def __init__(self, cards: deque[Card] = None):
        super().__init__(cards)
        if self: 
            self.cards[-1].flip()

    def take_cards(self, num: int) -> deque[Card]:
        cards = super().take_cards(num)
        for card in cards:
            if not card.is_opened:
                raise ValueError("Niektóre z wybranych kart są zakryte")

        if self and not self[-1].is_opened: 
            self[-1].flip()
        return cards

    def put_cards(self, cards: deque[Card]) -> None:
        if not self:
            # column is empty
            if cards[0].rank_num == 12:
                super().put_cards(cards)
            else:
                raise ValueError('Na puste pole można umiszczać tylko króla')
        elif ( 
            cards[0].rank_num + 1 == self[-1].rank_num 
            and 
            cards[0].color != self[-1].color
        ):
            # column is not empty
            super().put_cards(cards)
        else:
            raise ValueError(f"Nie pożna umieścic {cards[0].rank}{cards[0].suit} na {self[-1].rank}{self[-1].suit}")

    def draw(self, col: int, row: int) -> None:
        super().draw(col, row)
        for i, card in enumerate(self.cards):
            card.draw(col, row + i)

