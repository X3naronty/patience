from card import Card
from card_deck import CardDeck
from collections import deque
from table import Table
import re
import time
import sys, select
from reserve_stack import ReserveStack

def flush_stdin():
    while select.select([sys.stdin], [], [], 0)[0]:
        sys.stdin.readline()

class Game:
    def __init__(self):
        card_deck = CardDeck()
        cards = card_deck.cards

        self.table = Table(self, Game.take_cards(cards, 28))
        self.res_stack = ReserveStack(cards, "light")
        # end_stack = EndStack()
        # player = Player()
        
        self.is_running = False
    
    def run(self):
        self.is_running = True
        while self.is_running:
            # self.draw()
            player_input = input('Make your rush or type "help" to get manual:\n')
            self.handle(player_input)
    
    def format_player_input(self, player_input: str) -> str:
        formatted_input = re.sub(r'\s+', ' ', player_input.strip(" "))
        return formatted_input

    def handle(self, player_input: str) -> None:
        player_input = self.format_player_input(player_input)
        try:
            self.make_move(player_input)
        except (ValueError, IndexError) as e:
            print(e)
            print("Try again after 2s delay:")
            time.sleep(2)
            flush_stdin()
            
    def move_from_res_stack_to_column(self, col: int):
        card = self.res_stack.take_card()
        self.table.put_card_to_column(card, col)

    def make_move(self, move: str) -> None:
        match move:
            case move if re.fullmatch(r's_r\s>\s[1-7]', move):
                print("Przenieś ze stosu reserwowego do kolumny")
                col, = re.findall(r'[1-7]', move)
                self.move_from_res_stack_to_column(col)
            case move if re.fullmatch(r's_r\s>\ss_k', move):
                print("Ze stosu reserwowego do stosu końcowego")
            case move if re.fullmatch(r'[1-7]\s>\s[1-7]', move):
                print("Z kolumny do kolumny")
            case move if re.fullmatch(r'[1-7]\s>\ss_k', move):
                print("Z kolumny do stosu końcowego")
            case move if re.fullmatch(r'open\ss_r', move):
                print("Odkryj stos reserwowy")
            case move if re.fullmatch(r'reset\ss_r', move):
                print("Przetasuj stos reserwowry"                       )
            case move if re.fullmatch(r'help', move):
                print('This is help messsage')
            case _:
                raise ValueError('Wrong input:(')
        
        # self.player.count += 1


    @staticmethod    
    def take_cards(card_stack: deque[Card], num: int) -> deque[Card]:
        cards = deque([])
        try:
            for i in range(num):
                cards.append(card_stack.pop())
        except IndexError:
            print("There are not enough cards")
            time.sleep(1)
            flush_stdin()

        return cards
    
