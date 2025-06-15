# Console Solitaire

## Launch

### Requirements

1. Console has to support "ANSI Escape Sequences"
2. Console has to have "Nerd" font style set

Windows Terminal with default options matches all the requirements

Steps (in console):

1. Go to the root folder of the project
2. Execute: `python -m main` or `python main.py`

---

This is manual, write commands following all the spaces and characters:

Move from column to column:<br>
    (1 - 7) > (1 - 7) =(card count)<br>
    1 > 2 =3

Move from reserve pile to column:<br>
    s_r > (1 - 7)<br>
    s_r > 2

Move from reserve pile to column:<br>
    s_r > s_k

Shuffle reserve pile:<br>
    reset s_r

Open from reserve pile:<br>
    open s_r

Restart:<br>
    restart

Go back 1 step:<br>
    back

Quit:<br>
    quit
