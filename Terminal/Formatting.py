import os
import math

RESET = "\033[0m"
black =     lambda s, bg=False: f"\033[{4 if bg else 3}0m"+str(s)+RESET
red =       lambda s, bg=False: f"\033[{4 if bg else 3}1m"+str(s)+RESET
green =     lambda s, bg=False: f"\033[{4 if bg else 3}2m"+str(s)+RESET
yellow =    lambda s, bg=False: f"\033[{4 if bg else 3}3m"+str(s)+RESET
blue =      lambda s, bg=False: f"\033[{4 if bg else 3}4m"+str(s)+RESET
magenta =   lambda s, bg=False: f"\033[{4 if bg else 3}5m"+str(s)+RESET
cyan =      lambda s, bg=False: f"\033[{4 if bg else 3}6m"+str(s)+RESET
white =     lambda s, bg=False: f"\033[{4 if bg else 3}7m"+str(s)+RESET
default =   lambda s, bg=False: f"\033[{4 if bg else 3}9m"+str(s)+RESET

bold = lambda s:            "\033[1m"+str(s)+"\033[22m"
thin = lambda s:            "\033[2m"+str(s)+"\033[22m"
italic = lambda s:          "\033[3m"+str(s)+"\033[23m"
underline = lambda s:       "\033[4m"+str(s)+"\033[24m"
blink = lambda s:           "\033[5m"+str(s)+"\033[25m"
strikethrough = lambda s:   "\033[9m"+str(s)+"\033[29m"

hexcolor = lambda s, c, bg=False: f'\033[{48 if bg else 38};2;{int(c[0:2], 16)};{int(c[2:4], 16)};{int(c[4:6], 16)}m{s}{RESET}'

percentage = lambda val, max: f'\033[38;2;{int((255 * val)/max)};{int((255*(max-val))/max)};0m{int(val/max*100)}%{RESET}'

UP = "\033[A"
print_up = lambda s: print(f'{UP}{s}\r',)
DOWN = "\033[B"
RIGHT = "\033[C"
LEFT = "\033[D"

HIDE = "\033[?25l"
hide = lambda: print(HIDE, end="")
UNHIDE = "\033[?25h"
unhide = lambda: print(UNHIDE, end="")
CLEAR = "\033[0K"

h_line = lambda cols, spacing: (f'+{"-"*(spacing-1)}'*cols)+"+"
v_lines = lambda cols, spacing: f"|{DOWN}{LEFT}|{UP}{LEFT}{RIGHT*(spacing)}"*(cols+1)

class Table:

    def __init__(self, data:dict[str, str], header:str) -> None:
        self.width = os.get_terminal_size().columns-1
        self.data = data
        self.header = header

    def print(self, spacing = None, cols = None):
        spacing = sorted([len(str(item)) for item in list(self.data.values()) + list(self.data.keys())])[-1]+3 if spacing is None else spacing
        cols = (math.floor(self.width/spacing) if cols is None else cols) if len(self.data.keys())*spacing > self.width else len(self.data.keys())
        index = 0
        print(self.header)
        print(h_line(cols, spacing))
        for key, value in self.data.items():
            print(f'  {cyan(bold(key))}:{CLEAR}')
            print(f'{RIGHT*(index*spacing)}  {magenta(value)}{CLEAR}{UP}', end=f"\r{RIGHT*(index+1)*spacing}")
            index+=1
            if index == cols or key is list(self.data.keys())[-1]:
                print("\r"+v_lines(cols, spacing))
                print("\n"+h_line(cols, spacing))
                index = 0


if "main" in __name__:
    table = Table({f"test{i}":"test" for i in range(10)}, "test")
    table.print(8, 5)
    table.print()

    for i in range(11):
        print(percentage(i, 10))