from typing import List, Tuple

from agents.base import IntelligentBase
from agents.ghosts.base import ClassicGhostBase, GhostBase
from agents.pacman import PacmanBaseAgent
from ai.predictable import Predictable
from data.data import DIR, GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# pinky base class
class PinkyBaseAgent(GhostBase):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(POS.PINKY, REP.PINKY, 0, pf)


# classic ai agent for pinky
class ClassicAgent(PinkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(POS.PINKY, REP.PINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.PINKY_CORNER

        # chase mode
        targetTile: CPair = pacman.pos
        for _ in range(4):
            targetTile = targetTile.move(pacman.direction)

        # replicate target tile bug in classic pacman
        if pacman.direction == DIR.UP:
            for _ in range(4):
                targetTile = targetTile.move(DIR.LF)

        return targetTile


# classic aggressive ai agent for pinky
class ClassicAggrAgent(PinkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(POS.PINKY, REP.PINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        targetTile: CPair = pacman.pos
        for _ in range(4):
            targetTile = targetTile.move(pacman.direction)

        # replicate target tile bug in classic pacman
        if pacman.direction == DIR.UP:
            for _ in range(4):
                targetTile = targetTile.move(DIR.LF)

        return targetTile

    # get next postition of pinky (overrided for cruise elroy mode)
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


# neural q agent for pinky
class NeuralQAgent(PinkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.PINKY, REP.PINKY, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)


# neat agent for pinky
class NEATAgent(PinkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.PINKY, REP.PINKY, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)
