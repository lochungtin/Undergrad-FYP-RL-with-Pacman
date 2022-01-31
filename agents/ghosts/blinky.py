from typing import List, Tuple

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.game import Game

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
class BlinkyClassicAgent(BlinkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(self, POS.BLINKY, REP.BLINKY, 0, pf)

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
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair]:
        if self.mode == GHOST_MODE.CRUISE_ELROY:
            # generate path
            self.prevPath = self.path
            if self.pos != game.pacman.pos:
                self.path = self.pathfinder.start(self.pos, game.pacman.pos, self.direction)

                self.prevPos = self.pos
                self.pos = self.path.path[0]

            # update direction of travel
            if self.pos != self.prevPos:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos

        return super().getNextPos(game)


# classic aggressive ai agent for blinky
class BlinkyClassicAggrAgent(BlinkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(self, POS.BLINKY, REP.BLINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, pacman: PacmanBaseAgent, blinkyPos: CPair) -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        return pacman.pos

    # get next postition of blinky (overrided for cruise elroy mode)
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair]:
        if self.mode == GHOST_MODE.CRUISE_ELROY:
            # generate path
            self.prevPath = self.path
            if self.pos != game.pacman.pos:
                self.path = self.pathfinder.start(self.pos, game.pacman.pos, self.direction)

                self.prevPos = self.pos
                self.pos = self.path.path[0]

            # update direction of travel
            if self.pos != self.prevPos:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos

        return super().getNextPos(game)


# neural q agent for blinky
class BlinkyNeuralQAgent(BlinkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        BlinkyBaseAgent.__init__(self, None)
        IntelligentBase.__init__(self, POS.BLINKY, REP.BLINKY, predictable)

    def processState(self, game: "Game") -> List[int]:
        return super().processState(game)


# neat agent for blinky
class BlinkyNEATAgent(BlinkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        BlinkyBaseAgent.__init__(self, None)
        IntelligentBase.__init__(self, POS.BLINKY, REP.BLINKY, predictable)

    def processState(self, game: "Game") -> List[int]:
        return super().processState(game)
