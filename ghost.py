from constants import *
from movable import Movable


class Ghost(Movable):
    def __init__(self, pos, rep):
        super().__init__(pos, rep)

        self.mode = GHOST_MODE.CHASE

    def setMode(self, mode):
        self.mode = mode
