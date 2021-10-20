from typing import List, Tuple
import random

from data import DIR, GHOST_MODE, POS, REP
from game.components.movable.movable import Movable
from game.utils.path import Path
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Ghost(Movable):
    def __init__(self, pos: CPair, repId: int, dead: bool, pf: PathFinder) -> None:
        super().__init__(pos, repId)

        self.mode: int = GHOST_MODE.SCATTER
        self.isFrightened: bool = False
        self.speedReducer: int = 2

        self.pathfinder: PathFinder = pf
        self.path: Path = Path()

        self.dead: bool = dead

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        return CPair(1, 1)

    # get pacman's location from state
    def getPacmanPos(self, state: List[List[int]]) -> CPair:
        for rowIndex, row in enumerate(state):
            for colIndex, cell in enumerate(row):
                if cell == REP.PACMAN:
                    return CPair(rowIndex, colIndex)

        return CPair(1, 1)

    # modified version of getValidNeighbours to accomodate for "no go up" zones
    def getValidNeighbours(self, state: List[List[int]]) -> List[CPair]:
        rt: List[CPair] = []

        for index, pos in enumerate(self.pos.getValidNeighbours()):
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

        print(self.pos, rt)
        return rt

    # get next position of ghost
    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        # ignore if in house
        if self.dead:
            return self.pos, self.pos

        # update prev pos
        self.prevPos = self.pos

        # start random walk if frightened
        if self.isFrightened:
            # reverse direction for first step
            # hold position if reverse is invalid
            if self.speedReducer == 2:
                newPos = self.pos.move(DIR.getOpposite(self.direction))
                if newPos.isValid() and not REP.isWall(state[newPos.row][newPos.col]):
                    self.pos = newPos

                self.speedReducer = 1

            # slow down ghost speed (walk every 2 time steps)
            self.speedReducer = (self.speedReducer + 1) % 2
            if self.speedReducer == 0:
                self.pos = random.choice(self.getValidNeighbours(state))

        # normal behaviour
        else:
            # generate path
            self.path = self.pathfinder.start(
                self.pos, self.getTargetTile(state), self.direction
            ) 
            if len(self.path.path) > 0:
                self.pos = self.path.path[0]


        # update direction of travel
        if self.pos != self.prevPos:
            self.direction = self.pos.relate(self.prevPos)

        return self.pos, self.prevPos
