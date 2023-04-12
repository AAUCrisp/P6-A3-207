import time

class Clock:
    offset = 0

    def get(self) -> float:
        return time.time() + self.offset

    def set(self, value):
        self.offset = value - time.time()




if "main" in __name__:
    clock1 = Clock()
    clock2 = Clock()
    clock2.set(1)

    time.sleep(1)
    print(f'System clock:   {time.time()}')
    print(f'Clock 1:        {clock1.get()}')
    print(f'Clock 2:        {clock2.get()}')