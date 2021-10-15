from constants import *
from movable import Movable


class Ghost(Movable):
    def __init__(self, pos):
        super().__init__(pos)

        self.mode = GHOST_MODE.CHASE

    def setMode(self, mode):
        self.mode = mode
