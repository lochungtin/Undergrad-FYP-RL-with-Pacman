from typing import List, Tuple

from agents.base import IntelligentBase
from agents.ghosts.base import ClassicGhostBase, GhostBase
from agents.pacman import PacmanBaseAgent
from ai.predictable import Predictable
from data.data import GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# blinky base class
class BlinkyBaseAgent(GhostBase):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0, pf)


# classic ai agent for blinky
class ClassicAgent(BlinkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(POS.BLINKY, REP.BLINKY, 0, pf)

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


# classic aggressive ai agent for blinky
class ClassicAggrAgent(BlinkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(POS.BLINKY, REP.BLINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

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


# neural q agent for blinky
class NeuralQAgent(BlinkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.BLINKY, REP.BLINKY, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)


# neat agent for blinky
class NEATAgent(BlinkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.BLINKY, REP.BLINKY, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)
