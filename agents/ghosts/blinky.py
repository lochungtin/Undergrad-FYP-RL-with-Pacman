from typing import List, Tuple

from agents.ghosts.base import ClassicGhostBase
from agents.pacman import PacmanBaseAgent
from data.data import GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class ClassicAgent(ClassicGhostBase):
    def __init__(self, pos: CPair, repId: int, initWait: int, pf: PathFinder) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.BLINKY_CORNER

        # chase mode
        return pacman.pos

    # get next postition of blinky (overrided for cruise elroy mode)
    def getNextPos(
        self, state: List[List[int]], pacman: PacmanBaseAgent, blinkyPos: CPair
    ) -> Tuple[CPair, CPair]:
        if self.mode == GHOST_MODE.CRUISE_ELROY:
            # generate path
            self.prevPath = self.path
            self.path = self.pathfinder.start(self.pos, pacman.pos, self.direction)

            self.prevPos = self.pos
            self.pos = self.path.path[0]

            # update direction of travel
            if self.pos != self.prevPos:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos

        return super().getNextPos(state, pacman, blinkyPos)
