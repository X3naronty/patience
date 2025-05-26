from game import Game
from state_handler import StateHandler
import time
import sys 
import select
import datetime
import pickle
import os


def flush_stdin():
    while select.select([sys.stdin], [], [], 0)[0]:
        sys.stdin.readline()

class GameManager:
    def __init__(self):
        self._game = None
        self.is_running = False
        self.state_handler = StateHandler
        
    def format_input(self, player_input: str):
        return player_input.strip(' ')
    
    def start(self) -> None:
        self.reset()
        self.run()
        
    def reset(self) -> None:
        os.system('clear')
        self.is_running = True
        player_input = input('Enter game mode: "hard" or "light"\n')            
        mode = self.format_input(player_input)
        self._game = Game(mode)
        print(1)
        input('')
        
    def run(self):
        while(self.is_running):
            state = self._game.run()
            try:
                self.handle(state)
            except ValueError as e:
                print(e)
                print("Try again after 3s delay:)))")
                time.sleep(3)
                flush_stdin()

    def handle(self, state: str) -> None:
        match state:
            case "roll_back":
                new_game = Game.state_handler.take_previous_state()
                print(new_game.steps)
                input('')
                self._game = new_game
            case "restart":
                Game.state_handler.clear() 
                self.reset()
            case "game_over":
                steps = self._game.steps
                date = str(datetime.datetime.now()).rsplit('.', 1)[0]
                results = None
                try:
                    with open("results.pickle", "rb") as f:
                        results = pickle.load(f)
                        results.append((date, steps))
                        results = sorted(results, key=lambda x: x[-1])
                        print(')))')
                        input('')
                except (FileNotFoundError, EOFError):
                        results = [(date, steps)]
                finally:  
                    with open("results.pickle", "wb") as f:
                        print(12, results, f)
                        input('')
                        pickle.dump(results, f)
                    


                highlight = f'\u001b[48;2;50;0;0m'
                reset = f'\u001b[0m'
                for res in results: 
                    output = res[0] + '  --  ' + str(res[1])
                    if res[0] == date: output = highlight + output + reset
                    print(output)
                
                input("Naciśnij Enter żeby zacząć od nowa")
                self.reset()



                 
        
