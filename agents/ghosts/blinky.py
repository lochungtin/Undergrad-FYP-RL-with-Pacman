from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent
from data.data import GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# classic ai agent for blinky
class BlinkyClassicAgent(ClassicGhostAgent):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(self, POS.BLINKY, REP.BLINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.BLINKY_CORNER

        # chase mode
        return game.pacman.pos

    # get next postition of blinky (overrided for cruise elroy mode)
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
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
class BlinkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(self, POS.BLINKY, REP.BLINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        return game.pacman.pos

    # get next postition of blinky (overrided for cruise elroy mode)
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
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
