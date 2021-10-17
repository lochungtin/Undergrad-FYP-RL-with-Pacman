from data import *
from blinky import Blinky
from clyde import Clyde
from inky import Inky
from pinky import Pinky
from pacman import Pacman
from pellet import Pellet


class Game:
    def __init__(self):
        # set state to board layout
        self.state = REP.BOARD

        # create pacman and ghosts
        self.pacman = Pacman(POS.PACMAN)
        self.blinky = Blinky(POS.BLINKY)
        self.inky = Inky(POS.INKY)
        self.clyde = Clyde(POS.CLYDE)
        self.pinky = Pinky(POS.PINKY)

        self.movables = [self.pacman, self.blinky, self.inky, self.clyde, self.pinky]

        # create pellet objects
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

        self.pelletCount = DATA.TOTAL_PELLET_COUNT
        self.pwrpltCount = DATA.TOTAL_PWRPLT_COUNT

    def setState(self, pos, rep):
        self.state[pos[0]][pos[1]] = rep

    def nextState(self):
        # update pacman pos
        prev, cur = self.pacman.nextPos(self.state)

        self.state[prev[0]][prev[1]] = REP.EMPTY
        self.state[cur[0]][cur[1]] = REP.PACMAN

        # set pellet to not valid after visiting celL
        cellObj = self.pelletState[cur[0]][cur[1]]
        if cellObj != None and cellObj.valid:
            cellObj.destroy()

            if cellObj.rep == REP.PELLET:
                self.pelletCount -= 1
            else:
                self.pwrpltCount -= 1

        # update ghost positions

        # return gameover boolean
        if self.pelletCount + self.pwrpltCount == 0:
            return True

        return False
