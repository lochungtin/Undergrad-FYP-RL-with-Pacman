from typing import List, Tuple

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import IntelligentBase
from agents.ghosts.base import ClassicGhostBase, GhostBase
from agents.pacman import PacmanBaseAgent
from ai.predictable import Predictable
from data.data import DATA, DIR, GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# inky base class
class InkyBaseAgent(GhostBase):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(POS.INKY, REP.INKY, DATA.GHOST_EXIT_INTERVAL * 1, pf)


# classic ai agent for inky
class InkyClassicAgent(InkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(self, POS.INKY, REP.INKY, DATA.GHOST_EXIT_INTERVAL * 1, pf)

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
class InkyClassicAggrAgent(InkyBaseAgent, ClassicGhostBase):
    def __init__(self, pf: PathFinder) -> None:
        ClassicGhostBase.__init__(self, POS.INKY, REP.INKY, DATA.GHOST_EXIT_INTERVAL * 1, pf)

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


# neural q agent for inky
class InkyNeuralQAgent(InkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        InkyBaseAgent.__init__(self, None)
        IntelligentBase.__init__(self, POS.INKY, REP.INKY, predictable)

    def processState(self, game: "Game") -> List[int]:
        return super().processState(game)


# neat agent for inky
class InkyNEATAgent(InkyBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        InkyBaseAgent.__init__(self, None)
        IntelligentBase.__init__(self, POS.INKY, REP.INKY, predictable)

    def processState(self, game: "Game") -> List[int]:
        return super().processState(game)
