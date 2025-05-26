from card import Card
from card_deck import CardDeck
from collections import deque
from table import Table
import re
import time
import sys
import select
from reserve_pile import ReservePile
from end_piles_area import EndPilesArea
import os
import pickle
from os.path import join
from state_handler import StateHandler
import copy

def flush_stdin():
    while select.select([sys.stdin], [], [], 0)[0]:
        sys.stdin.readline()

HELP_MESSAGE = '''
This is help message, type comands respecting all spaces and other symbols

Przenieść z kolumny do kolumny:
    (1 - 7) > (1 - 7) =(ilość kart)
    1 > 2 =3

Przenieść ze stosu reserwowego do kolumhy:
    s_r > (1 - 7)
    s_r > 2

Przenieść ze stosu reserwowego do stosu końcowego:
    s_r > s_k

Przetasować stos reserwowy:                                                         
    reset s_r                                                                   
                                                                                    
Odkryć stos reserwowy:                                                               
    open s_r                                                                        

'''


class Game:
    columns, rows = os.get_terminal_size()
    bg = '\u001b[48;2;0;105;0m'  # green background
    reset = '\u001b[0m'
    state_handler = StateHandler()

    def __init__(self, mode: str = "light"):
        card_deck = CardDeck()
        self.card_count = CardDeck.card_count
        self.table = Table(card_deck.take_cards(Table.cards_required))
        self.res_pile = ReservePile(card_deck.take_cards(len(card_deck)), mode)
        self.end_piles = EndPilesArea()
        

        self.steps = 0

        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            self.draw()
            Game.state_handler.save_state(self)

            input_offset = f'\u001b[{len(max(self.table.columns, key=len)) + 10};1f'
            player_input = input(
                f'\n\n{self.bg}{input_offset}Make your rush or type "help" to get manual:\n')
            new_state = self.handle(player_input)
            if new_state != "continue":
                print(new_state)
                input('')
                return new_state
        
    def draw(self):
        # Fill screen with background
        for _ in range(self.rows):
            print(f'{self.bg}{" " * self.columns}{self.reset}')
    
        self.res_pile.draw(1, 1)
        self.end_piles.draw(30, 1)
        self.table.draw(7, 7)

    def format_player_input(self, player_input: str) -> str:
        formatted_input = re.sub(r'\s+', ' ', player_input.strip(" "))
        return formatted_input

    def handle(self, player_input: str) -> str:
        player_input = self.format_player_input(player_input)
        try:
            new_state = self.make_move(player_input)
            return new_state
        except (ValueError) as e:
            print(e)
            print("Try again after 3s delay:")
            time.sleep(3)
            flush_stdin()
            return 'roll_back'

    def move_from_res_pile_to_column(self, col: int):
        card = self.res_pile.take_card()
        self.table.put_cards_to_column(deque([card]), col)

    def move_from_res_pile_to_end_pile(self):
        card = self.res_pile.take_card()
        self.end_piles.put_card(card)

    def move_from_col_to_col(self, col_1: int, col_2: int, num: int):
        cards = self.table.take_cards_from_column(num, col_1)
        cards.reverse()
        self.table.put_cards_to_column(cards, col_2) 
        
    def move_from_col_to_end_pile(self, col: int): 
        card , = self.table.take_cards_from_column(1, col)
        self.end_piles.put_card(card)

    def make_move(self, move: str) -> str:
        match move:
            case move if re.fullmatch(r's_r\s>\s[1-7]', move):
                print("Przenieś ze stosu reserwowego do kolumny")
                col, = re.findall(r'[1-7]', move)
                col = int(col)
                self.move_from_res_pile_to_column(col)
            case move if re.fullmatch(r's_r\s>\ss_k', move):
                print("Ze stosu reserwowego do stosu końcowego")
                self.move_from_res_pile_to_end_pile()
                
                if self.end_piles.get_card_count() == self.card_count:
                    return "game_over"
            case move if re.fullmatch(r'[1-7]\s>\s[1-7]\s=(1[0-3]|[1-9])', move):
                col_1, col_2 = re.findall(r'[1-7]', move[:5])
                num, = re.findall(r'=(1[0-3]|[1-9])', move[5:])
                col_1, col_2, num = int(col_1), int(col_2), int(num)
                print("Z kolumny do kolumny")
                self.move_from_col_to_col(col_1, col_2, num)
            case move if re.fullmatch(r'[1-7]\s>\ss_k', move):
                print("Z kolumny do stosu końcowego")
                col , = re.findall(r'[1-7]', move)
                col = int(col)
                self.move_from_col_to_end_pile(col)
                
                if self.end_piles.get_card_count() == self.card_count:
                    return "game_over"
            case move if re.fullmatch(r'open\ss_r', move):
                print("Odkryj stos reserwowy")
                self.res_pile.open_cards()
            case move if re.fullmatch(r'reset\ss_r', move):
                print("Przetasuj stos reserwowry")
                self.res_pile.reset()
            case move if re.fullmatch(r'help', move):
                print(HELP_MESSAGE)
                input('Naciśnij coś any kontynuować')
            case move if re.fullmatch(r'back', move):
                Game.state_handler.take_previous_state()
                return "roll_back"
            case move if re.fullmatch(r'restart', move):
                return "restart"
            case move if re.fullmatch(r'finish', move):
                return 'game_over'
            case _:
                raise ValueError('Wrong input:(')
        self.steps += 1
        return "continue"
        


    
