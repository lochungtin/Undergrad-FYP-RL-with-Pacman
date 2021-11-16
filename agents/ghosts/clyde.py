from typing import List

from agents.base import IntelligentBase
from agents.ghosts.base import ClassicGhostBase, GhostBase
from agents.pacman import PacmanBaseAgent
from ai.predictable import Predictable
from data.data import DATA, GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# clyde base class
class ClydeBaseAgent(GhostBase):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(POS.CLYDE, REP.CLYDE, DATA.GHOST_EXIT_INTERVAL * 2, pf)


# classic ai agent for clyde
class ClassicAgent(ClydeBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(
            self, POS.CLYDE, REP.CLYDE, DATA.GHOST_EXIT_INTERVAL * 2, pf
        )

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.CLYDE_CORNER

        # chase mode
        if len(self.pathfinder.start(self.pos, pacman.pos, self.direction).path) < 8:
            return POS.CLYDE_CORNER

        return pacman.pos


# classic aggressive ai for clyde
class ClassicAggrAgent(ClydeBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(
            self, POS.CLYDE, REP.CLYDE, DATA.GHOST_EXIT_INTERVAL * 2, pf
        )

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        if len(self.pathfinder.start(self.pos, pacman.pos, self.direction).path) < 8:
            return POS.CLYDE_CORNER

        return pacman.pos


# neural q agent for clyde
class NeuralQAgent(ClydeBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.CLYDE, REP.CLYDE, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)


# neat agent for clyde
class NEATAgent(ClydeBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.CLYDE, REP.CLYDE, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        return super().processState(state)
