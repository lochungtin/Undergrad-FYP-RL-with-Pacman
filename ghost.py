from constants import *
from movable import Movable


class Ghost(Movable):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.mode = GHOST_MODE.CHASE

    def setMode(self, mode):
        self.mode = mode
