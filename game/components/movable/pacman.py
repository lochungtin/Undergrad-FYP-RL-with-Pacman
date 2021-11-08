from typing import List, Tuple

from data import DIR, POS, REP
from game.components.movable.movable import Movable
from utils.coordinate import CPair


class Pacman(Movable):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)

    # get next position of pacman
    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        newPos: CPair = self.pos.move(self.direction)
        self.moved = False

        # special cases (looping)
        if newPos == POS.LEFT_LOOP_TRIGGER:
            self.prevPos = self.pos
            self.pos = POS.RIGHT_LOOP
            self.moved = True

        elif newPos == POS.RIGHT_LOOP_TRIGGER:
            self.prevPos = self.pos
            self.pos = POS.LEFT_LOOP
            self.moved = True

        # natural movement
        elif newPos.isValid() and not REP.isWall(state[newPos.row][newPos.col]):
            self.prevPos = self.pos
            self.pos = newPos
            self.moved = True

        return self.pos, self.prevPos

    # set direction
    def setDir(self, direction: int) -> None:
        self.direction: int = direction
