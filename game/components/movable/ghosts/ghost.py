from typing import List, Tuple

from data import GHOST_MODE
from game.components.movable.movable import Movable
from game.utils.path import Path
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Ghost(Movable):
    def __init__(self, pos: CPair, repId: int, inHouse: bool, pathfinder: PathFinder) -> None:
        super().__init__(pos, repId)

        self.mode: int = GHOST_MODE.CHASE
        self.steps: int = 200

        self.pathfinder: PathFinder = pathfinder
        self.path: Path = Path()

        self.inHouse: bool = inHouse

    # set ghost movement mode and step counter
    def setMode(self, mode: int, steps: int) -> None:
        self.mode: int = mode
        self.steps: int = steps

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        return CPair(1, 1)

    # get next position of ghost
    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        if self.inHouse:
            return self.pos, self.pos

        self.path = self.pathfinder.start(self.pos, self.getTargetTile(state), self.direction)

        self.prevPos = self.pos
        if len(self.path.path) > 0:
            self.pos = self.path.path[0]

        # update direction of travel
        self.direction = self.pos.relate(self.prevPos)
        print(self.direction)

        return self.pos, self.prevPos
