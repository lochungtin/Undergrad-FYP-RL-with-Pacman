from constants import *
from ghost import Ghost


class Pinky(Ghost):
    def __init__(self, pos):
        super().__init__(pos, REP.PINKY)

    def nextPos(self, state):
        return self.prevPos, self.pos
        