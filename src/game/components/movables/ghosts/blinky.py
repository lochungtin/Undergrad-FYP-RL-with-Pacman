from .....data.constants import *
from .ghost import Ghost


class Blinky(Ghost):
    def __init__(self, pos):
        super().__init__(pos, REP.BLINKY)

    def nextPos(self, state):
        return self.prevPos, self.pos
        