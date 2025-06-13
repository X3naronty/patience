import os
import re

class CLI:
    bg = '\u001b[48;2;0;105;0m'  # green background
    reset = '\u001b[0m'

    def __init__(self, required_cols = None, required_rows = None):
        cols, rows = os.get_terminal_size()
        if (
            required_cols and cols < required_cols
            or 
            required_rows and rows < required_rows
        ):
            raise ValueError("Console window is too small")
        self.cols = cols
        self.rows = rows

    def draw_background(self, color = None, cols = None, rows = None):
        # move to the top left corner 
        print('\u001b[1;1f', end='')

        if not color: color = self.bg
        if not cols: cols = self.cols
        if not rows: rows = self.rows

        # Fill screen with background
        for _ in range(rows):
            print(f'{color}{" " * cols}{self.reset}')

        # move to the top left corner
        print('\u001b[1;1f', end='')

    
    def format_input(self, player_input: str) -> str:
        formatted_input = re.sub(r'\s+', ' ', player_input.strip(" "))
        return formatted_input
    

    def handle_error(self, error: ValueError) -> None:
        print(error)
        input('Press Enter to continue')




