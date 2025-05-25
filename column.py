from collections import deque
from card import Card
from card_pile import CardPile


class Column(CardPile):
    def __init__(self, cards: deque[Card] = None):
        super().__init__(cards)
        if self: self._cards[-1].flip()

    def take_cards(self, num: int) -> deque[Card]:
        cards = super()._take_cards(num)
        for card in cards:
            if not card.is_opened:
                raise ValueError("You can't take this card, because it's closed")

        if self and not self[-1].is_opened: self[-1].flip()
        return cards

    def put_cards(self, cards: deque[Card]) -> None:
        if not self:
            if cards[0].rank_num == 12:
                super()._put_cards(cards)
            else:
                raise ValueError('You can put only king to the empty field')
        elif ( 
            cards[0].rank_num + 1 == self[-1].rank_num 
            and 
            cards[0].color != self[-1].color
        ):
            super()._put_cards(cards)
        else:
            raise ValueError(f"You can't put card {cards[0].rank}{cards[0].suit} on {self[-1].rank}{self[-1].suit}")

    def draw(self, col: int, row: int) -> None:
        super().draw(col, row)
        for i, card in enumerate(self._cards):
            card.draw(col, row + i)


if __name__ == "__main__":
    a = Column(
        deque([
            Card('Ace', 'spades', 0),
            Card('Quin', 'clubs', 11),
            Card('King', 'heartes', 12) 
        ])
    )
    b = Column()
    # a.draw(1, 1)
    # b.draw(5, 1)
    
    card_1 = Card('Ace', 'spades', 0)
    card_2 = Card('Ace', 'clubs', 0)
    card_3 = Card('King', 'heartes', 12) 

    cards = a.take_cards(1)
    b.put_cards(cards)

    cards = a.take_cards(1)
    b.put_cards(cards)
    
    

    a.draw(1, 1)
    b.draw(5, 1)
    input('')