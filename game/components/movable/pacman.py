from typing import List, Tuple

from data import DIR, REP
from game.components.movable.movable import Movable
from utils.coordinate import CPair


class Pacman(Movable):
    def __init__(self, pos: CPair) -> None:
        super().__init__(pos, REP.PACMAN)

        self.direction: int = DIR.UP

    # get next position of pacman
    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        newPos: CPair = self.pos.move(self.direction)

        # special cases (looping)
        if newPos.row == 14 and newPos.col == -1:
            self.prevPos = self.pos
            self.pos = CPair(14, 26)
        elif newPos.row == 14 and newPos.col == 27:
            self.prevPos = self.pos
            self.pos = CPair(14, 0)

        # natural movement
        elif newPos.isValid() and not REP.isWall(state[newPos.row][newPos.col]):
            self.prevPos = self.pos
            self.pos = newPos

        return self.pos, self.prevPos

    # set direction
    def setDir(self, direction: int) -> None:
        self.direction = direction
