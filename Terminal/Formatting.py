import os
import math

RESET = "\033[0m"
black = lambda s: "\033[30m"+str(s)+RESET
red = lambda s: "\033[31m"+str(s)+RESET
green = lambda s: "\033[32m"+str(s)+RESET
yellow = lambda s: "\033[33m"+str(s)+RESET
blue = lambda s: "\033[34m"+str(s)+RESET
magenta = lambda s: "\033[35m"+str(s)+RESET
cyan = lambda s: "\033[36m"+str(s)+RESET
white = lambda s: "\033[37m"+str(s)+RESET
default = lambda s: "\033[39m"+str(s)+RESET

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

class Table:
    def __init__(self, data:dict[str, str], header:str) -> None:
        self.width = os.get_terminal_size().columns
        self.data = data
        self.header = header

    def print(self, spacing=25):
        print(" "*(int(self.width/2)-(int(len(self.header)/2)))+f'{self.header}\n'+"-"*self.width)
        cols = math.floor(self.width/spacing)
        index = 0
        for key in self.data.keys():
            value = self.data[key]
            if index == cols:
                print(f'\r{RIGHT*self.width}|{DOWN}|', end="")
                print("\n"+"-"*self.width)
                index = 0
            print(f'| {cyan(key)}:')
            print(f'{RIGHT*(index*spacing)}| {magenta(value)}{UP}', end=f"\r{RIGHT*(index+1)*spacing}")
            index+=1
        print(f'\r{RIGHT*self.width}|{DOWN}|', end="")
        print("\n"+"-"*self.width)


if "main" in __name__:
    table = Table({f"test{i}":"test" for i in range(100)}, "test")
    table.print()