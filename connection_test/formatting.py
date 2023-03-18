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