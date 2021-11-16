from typing import List, Tuple

from agents.base import IntelligentBase
from agents.ghosts.base import ClassicGhostBase, GhostBase
from agents.pacman import PacmanBaseAgent
from ai.predictable import Predictable
from data.data import DIR, GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# inky base class
class InkyBaseAgent(GhostBase):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(POS.INKY, REP.INKY, 0, pf)


# classic ai agent for inky
class ClassicAgent(InkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(self, POS.INKY, REP.INKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.INKY_CORNER
            
        # chase mode
        # get reflection tile
        pivot: CPair = pacman.pos
        for _ in range(4):
            pivot = pivot.move(pacman.direction)

        # replicate target tile bug in classic pacman
        if pacman.direction == DIR.UP:
            for _ in range(4):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return blinkyPos.reflect(pivot)


# classic aggressive ai agent for inky
class ClassicAggrAgent(InkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(self, POS.INKY, REP.INKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        # get reflection tile
        pivot: CPair = pacman.pos
        for _ in range(4):
            pivot = pivot.move(pacman.direction)

        # replicate target tile bug in classic pacman
        if pacman.direction == DIR.UP:
            for _ in range(4):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return blinkyPos.reflect(pivot)

    # get next postition of inky (overrided for cruise elroy mode)
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


# neural q agent for inky
class NeuralQAgent(InkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.INKY, REP.INKY, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)


# neat agent for inky
class NEATAgent(InkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.INKY, REP.INKY, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)
