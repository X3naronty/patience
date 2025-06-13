import re
from collections import deque

from card_deck import CardDeck
from cli import CLI
from end_piles_area import EndPilesArea
from reserve_pile import ReservePile
from state_handler import StateHandler
from table import Table




class Game(CLI):
    state_handler = StateHandler()

    def __init__(self, mode: str = "light", required_cols = None, required_rows = None):
        super().__init__(required_cols, required_rows)
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
            Game.state_handler.save_state(self)
            self.draw()

            input_offset = f'\u001b[{len(max(self.table.columns, key=len)) + 10};1f'
            player_input = input(
                f'\n\n{self.bg}{input_offset}Make a move or type "help" to get manual:\n')
            new_status = self.handle(player_input)
            if new_status != "continue":
                return new_status
        
    def draw(self):
        self.draw_background()
    
        self.res_pile.draw(1, 1)
        self.end_piles.draw(30, 1)
        self.table.draw(7, 7)


    def handle(self, player_input: str) -> str:
        player_input = self.format_input(player_input)
        try:
            new_status = self.make_move(player_input)
            return new_status
        except ValueError as e:
            self.handle_error(e)
            return 'roll_back'

    def move_from_res_pile_to_column(self, move: str):
        col , = re.findall(r'[1-7]', move)
        col = int(col)

        card = self.res_pile.take_card()
        self.table.put_cards_to_column(deque([card]), col)

    def move_from_res_pile_to_end_pile(self):
        card = self.res_pile.take_card()
        self.end_piles.put_card(card)

    def move_from_col_to_col(self, move: str):
        col_1, col_2 = re.findall(r'[1-7]', move[:5])
        num , = re.findall(r'=(1[0-3]|[1-9])', move[5:])
        col_1, col_2, num = int(col_1), int(col_2), int(num)

        cards = self.table.take_cards_from_column(num, col_1)
        cards.reverse()
        self.table.put_cards_to_column(cards, col_2) 
        
    def move_from_col_to_end_pile(self, move: str): 
        col , = re.findall(r'[1-7]', move)
        col = int(col)
        card , = self.table.take_cards_from_column(1, col)
        self.end_piles.put_card(card)

    def make_move(self, move: str) -> str:
        match move:
            case move if re.fullmatch(r's_r\s>\s[1-7]', move):
                # Move from reserve pile column
                self.move_from_res_pile_to_column(move)
            case move if re.fullmatch(r's_r\s>\ss_k', move):
                # Move from reserve pile to end pile
                self.move_from_res_pile_to_end_pile()

                # Check game over 
                if self.end_piles.get_card_count() == self.card_count:
                    return "game_over"
            case move if re.fullmatch(r'[1-7]\s>\s[1-7]\s=(1[0-3]|[1-9])', move):
                # Move from column to column
                self.move_from_col_to_col(move)
            case move if re.fullmatch(r'[1-7]\s>\ss_k', move):
                # Move from column to end pile
                self.move_from_col_to_end_pile(move)

                # check game over 
                if self.end_piles.get_card_count() == self.card_count:
                    return "game_over"
            case move if re.fullmatch(r'open\ss_r', move):
                # Open cards from reserve pile
                self.res_pile.open_cards()
            case move if re.fullmatch(r'reset\ss_r', move):
                # Shuffle reserve pile
                self.res_pile.reset()
            case move if re.fullmatch(r'help', move):
                # Help
                return 'help'
            case move if re.fullmatch(r'back', move):
                # Step back

                # remove current state
                Game.state_handler.take_previous_state()

                return "roll_back"
            case move if re.fullmatch(r'restart', move):
                return "restart"
            # case move if re.fullmatch(r'finish', move):   # for debug, finishes the game
            #     return 'game_over'
            case move if re.fullmatch(r'quit', move):
                return 'quit'
            case _:
                raise ValueError('Wrong input:(')
        self.steps += 1
        return "continue"
        


    
