class PlayingArea:
    field_style = '\u001b[38;2;255;255;255m'
    reset = '\u001b[0m'
    field_icon = (
        '🭽▔▔🭾',
        '▏  ▕',
        '🭼▁▁🭿'
    )

    def __init__(self):
        pass
    
    @staticmethod 
    def draw_card_field(col: int, row: int) -> None:
        field_icon = PlayingArea.field_icon
        for i, r in enumerate(field_icon):
            print(
                f'\u001b[{i+row};{col}H' +
                f'{PlayingArea.field_style}' +
                f'{r}' +
                f'{PlayingArea.reset}'
            )

             

# PlayingArea.draw_card_field(10, 1)