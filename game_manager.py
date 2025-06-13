import datetime
import os
import pickle
import platform

from game import Game
from state_handler import StateHandler
from cli import CLI

HELP_MESSAGE = '''
This is manual, write commands following all the spaces and characters:

Move from column to column:
    (1 - 7) > (1 - 7) =(card count)
    1 > 2 =3

Move from reserve pile to column:
    s_r > (1 - 7)
    s_r > 2

Move from reserve pile to column:
    s_r > s_k

Shuffle reserve pile:
    reset s_r

Open from reserve pile:
    open s_r

Restart:
    restart

Go back 1 step:
    back

Quit:
    quit
'''

def clear_terminal():
    os_name = platform.system()
    if os_name == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


class GameManager(CLI):

    def __init__(self, required_cols = None, required_rows = None):
        super().__init__(required_cols, required_rows)
        self._game = None
        self.is_running = False
        self.state_handler = StateHandler
    
    def start(self) -> None:
        status_code = None
        while status_code != 0:
            try:
                status_code = self.create_game()
            except ValueError as e:
                print(status_code)
                self.handle_error(e)
                
        self.run()
        
    def create_game(self) -> int:
        os.system('clear')
        self.is_running = True
        self.draw_background()
        player_input = input(self.bg + 'Enter hardness level "hard" or "light"\n')
        mode = self.format_input(player_input)

        self._game = Game(mode, 50, 25)
        
        return 0
        
    def run(self):
        while self.is_running:
            state = self._game.run()
            try:
                self.handle(state)
            except ValueError as e:
                self.handle_error(e)

    def draw_help_message(self):
        cols = self.cols
        for line in HELP_MESSAGE.splitlines():
            background = f'{self.bg}{' ' * cols}'
            reset = self.reset
            print(background + '\r' + line + reset)
            
    def handle_game_over(self):
        steps = self._game.steps
        date = str(datetime.datetime.now()).rsplit('.', 1)[0]
        results = None
        try:
            with open("results.pickle", "rb") as f:
                results = pickle.load(f)
                results.append((date, steps))
                results = sorted(results, key=lambda x: x[-1])
        except (FileNotFoundError, EOFError):
                results = [(date, steps)]
        finally:  
            with open("results.pickle", "wb") as f:
                pickle.dump(results, f)
            
        print('\n\nGame over :))')
        print('Wynik: ')

        highlight = '\u001b[48;2;50;0;0m'
        bg = self.bg
        reset = self.reset
        for res in results: 
            output = res[0] + '  --  ' + str(res[1])
            if res[0] == date: 
                output = highlight + output + reset
            else:
                output = bg + output + reset
            print(output)
        
        input(bg + "Naciśnij Enter żeby zacząć od nowa")
        self.create_game()

    def handle(self, status: str) -> None:
        match status:
            case "roll_back":
                previous_game_state = Game.state_handler.take_previous_state()
                self._game = previous_game_state
            case "restart":
                Game.state_handler.clear() 
                self.start()
            case 'help':
                clear_terminal()
                self.draw_help_message()

                input(f'{self.bg}{' ' * self.cols}' + '\r' + 'Naciśnij Enter, aby contynuować' + self.reset)
            case "game_over":
                self.handle_game_over()
            case "quit":
                self.is_running = False

                # clear terminal
                cols, rows = os.get_terminal_size()
                self.draw_background(self.reset, cols, rows)



                 
        
