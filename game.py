from blinky import Blinky
from clyde import Clyde
from constants import *
from inky import Inky
from pacman import Pacman
from pinky import Pinky
from pellet import Pellet


class Game:
    def __init__(self):
        self.state = REP.BOARD

        self.pacman = Pacman(POS.PACMAN)
        self.blinky = Blinky(POS.BLINKY)
        self.inky = Inky(POS.INKY)
        self.clyde = Clyde(POS.CLYDE)
        self.pinky = Pinky(POS.PINKY)

        self.movables = [self.pacman, self.blinky, self.inky, self.clyde, self.pinky]

        self.pelletState = []

        for y, row in enumerate(REP.PELLET_BOARD):
            pelletRow = []
            for x, cell in enumerate(row):
                if cell == REP.EMPTY:
                    pelletRow.append(None)
                elif cell == REP.PELLET:
                    pelletRow.append(Pellet((y, x), REP.PELLET))
                else:
                    pelletRow.append(Pellet((y, x), REP.PWRPLT))

            self.pelletState.append(pelletRow)

    def setState(self, pos, rep):
        self.state[pos[0]][pos[1]] = rep

    def nextState(self):
        # update pacman pos
        prev, cur = self.pacman.nextPos(self.state)

        self.state[prev[0]][prev[1]] = REP.EMPTY
        self.state[cur[0]][cur[1]] = REP.PACMAN

        # update pellet validity
        cellObj = self.pelletState[cur[0]][cur[1]];
        if cellObj != None and cellObj.valid:
            cellObj.destroy()

        #
