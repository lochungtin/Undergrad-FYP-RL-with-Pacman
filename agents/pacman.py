from random import randint
from typing import List, Tuple

from agents.base import Base, IntelligentBase
from ai.predictable import Predictable
from data.data import DIR, POS, REP
from utils.coordinate import CPair


# pacman base agent
class PacmanBaseAgent(Base):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


# playable keyboard agent for pacman
class PlayableAgent(PacmanBaseAgent):
    def __init__(self) -> None:
        super().__init__()

        # initialise direction
        self.direction = DIR.UP

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


# neat agent for pacman
class NEATAgent(IntelligentBase, PacmanBaseAgent):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(POS.PACMAN, REP.PACMAN, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        input = []
        for i in range(10):
            input.append(randint(1, 10))

        return input
