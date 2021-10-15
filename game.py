from blinky import Blinky
from clyde import Clyde
from constants import *
from inky import Inky
from pacman import Pacman
from pinky import Pinky
from pwrpellet import PwrPlt


class Game:
    def __init__(self):
        self.state = REP.BOARD

        self.pacman = Pacman(POS.PACMAN)
        self.blinky = Blinky(POS.BLINKY)
        self.inky = Inky(POS.INKY)
        self.clyde = Clyde(POS.CLYDE)
        self.pinky = Pinky(POS.PINKY)

        self.movables = [self.pacman, self.blinky, self.inky, self.clyde, self.pinky]

        self.pwrpltTL = PwrPlt(POS.PWRPLTTL)
        self.pwrpltTR = PwrPlt(POS.PWRPLTTR)
        self.pwrpltBL = PwrPlt(POS.PWRPLTBL)
        self.pwrpltBR = PwrPlt(POS.PWRPLTBR)

        self.pwrplts = [self.pwrpltTL, self.pwrpltTR, self.pwrpltBL, self.pwrpltBR]

    def setState(self, pos, rep):
        self.state[pos[0]][pos[1]] = rep

    def nextState(self):
        # update pacman pos
        prev, cur = self.pacman.nextPos(self.state)

        self.state[prev[0]][prev[1]] = REP.EMPTY
        self.state[cur[0]][cur[1]] = REP.PACMAN

        #
