from typing import List, Tuple

from data import GHOST_MODE
from game.components.movable.movable import Movable
from game.utils.path import Path
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Ghost(Movable):
    def __init__(self, pos: CPair, repId: int, dead: bool, pf: PathFinder) -> None:
        super().__init__(pos, repId)

        self.mode: int = GHOST_MODE.SCATTER
        self.isFrightened: bool = False

        self.pathfinder: PathFinder = pf
        self.path: Path = Path()

        self.dead: bool = dead

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        return CPair(1, 1)

    # get next position of ghost
    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        # ignore if in house
        if self.dead:
            return self.pos, self.pos

        # generate path
        self.path = self.pathfinder.start(
            self.pos, self.getTargetTile(state), self.direction
        )

        # TO BE CHANGED (affects scatter mode looping)
        self.prevPos = self.pos
        if len(self.path.path) > 0:
            self.pos = self.path.path[0]

        # update direction of travel
        self.direction = self.pos.relate(self.prevPos)

        return self.pos, self.prevPos
