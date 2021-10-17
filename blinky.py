from data import *
from ghost import Ghost


class Blinky(Ghost):
    def __init__(self, pos):
        super().__init__(pos, REP.BLINKY)
