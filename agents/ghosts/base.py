from copy import deepcopy
from random import random
from typing import List, Tuple

from agents.base import Base
from agents.pacman import PacmanBaseAgent
from data.data import DATA, DIR, GHOST_MODE, POS, REP
from game.utils.path import Path
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair

# base class for ghost implementations (classic and intelligent)
class GhostBase(Base):
    def __init__(self, pos: CPair, repId: int, initWait: int, pf: PathFinder) -> None:
        super().__init__(pos, repId)

        self.mode: int = GHOST_MODE.SCATTER
        self.isDead: bool = False
        self.isFrightened: bool = False
        self.speedReducer: int = 2

        self.pathfinder: PathFinder = pf
        self.path: Path = Path()
        self.prevPath: Path = Path()

        self.initWait: int = initWait

    # modified version of getNeighbours to accomodate for "no go up" zones
    def getNeighbours(self, state: List[List[int]]) -> List[CPair]:
        rt: List[CPair] = []

        for index, pos in enumerate(self.pos.getNeighbours()):
            if (
                (
                    pos == POS.GHOST_NO_UP_1
                    or pos == POS.GHOST_NO_UP_2
                    or pos == POS.GHOST_NO_UP_3
                    or pos == POS.GHOST_NO_UP_4
                )
                and index == 0
                or REP.isWall(state[pos.row][pos.col])
                or DIR.getOpposite(self.direction) == index
            ):
                continue

            rt.append(pos)

        return rt

    # perform normal behaviour for next step
    def updatePositions(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> None:
        raise NotImplementedError

    # get next position of ghost
    def getNextPos(
        self, state: List[List[int]], pacman: PacmanBaseAgent, blinkyPos: CPair
    ) -> Tuple[CPair, CPair]:
        # wait at ghost house
        if self.initWait > -1:
            self.initWait -= 1
            return self.pos, self.pos

        # dead and returned to ghost house
        if self.isDead and self.pos == POS.GHOST_HOUSE_CENTER:
            self.isDead = False

        # start random walk if frightened
        if self.isFrightened:
            # update prev pos
            self.prevPos = self.pos

            # reverse direction for first step
            # hold position if reverse is invalid
            if self.speedReducer == DATA.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE:
                newPos = self.pos.move(DIR.getOpposite(self.direction))
                if newPos.isValid() and not REP.isWall(state[newPos.row][newPos.col]):
                    self.pos = newPos

                self.speedReducer = DATA.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE - 1

            # slow down ghost speed
            self.speedReducer = (
                self.speedReducer + 1
            ) % DATA.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE
            if self.speedReducer == 0:
                self.pos = random.choice(self.getNeighbours(state))

        # normal behaviour
        else:
            self.updatePositions(pacman, blinkyPos)

        # update direction of travel
        if self.pos != self.prevPos:
            self.direction = self.pos.relate(self.prevPos)

        return self.pos, self.prevPos


# base class for ghost implementations
class ClassicGhostBase(GhostBase):
    def __init__(self, pos: CPair, repId: int, initWait: int, pf: PathFinder) -> None:
        super().__init__(pos, repId, initWait, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        raise NotImplementedError

    # perform normal behaviour for next step
    def updatePositions(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> None:
        # get target tile
        targetTile: CPair = self.getTargetTile(pacman, blinkyPos)
        if self.pos == targetTile:
            targetTile = self.prevPos

        # generate path
        self.prevPath = self.path
        self.path = self.pathfinder.start(self.pos, targetTile, self.direction)

        self.prevPos = self.pos
        if len(self.path.path) > 0:
            self.pos = self.path.path[0]
