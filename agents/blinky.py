from typing import List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair


# classic ai agent for blinky
class BlinkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0)

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
        if game.pelletProgress < BOARD.CRUISE_ELROY_TRIGGER and not self.isDead:
            # generate path
            self.prevPath = self.path
            if self.pos != game.pacman.pos:
                self.path = self.pathfinder.start(self.pos, game.pacman.pos, self.direction)

                self.prevPos = self.pos
                self.pos = self.path[0]

            # update direction of travel
            if self.pos != self.prevPos:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos, True

        return super().getNextPos(game)


# classic aggressive ai agent for blinky
class BlinkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        return game.pacman.pos

    # get next postition of blinky (overrided for cruise elroy mode)
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        if game.pelletProgress < BOARD.CRUISE_ELROY_TRIGGER and not self.isDead:
            # generate path
            self.prevPath = self.path
            if self.pos != game.pacman.pos:
                self.path = self.pathfinder.start(self.pos, game.pacman.pos, self.direction)

                self.prevPos = self.pos
                self.pos = self.path[0]

            # update direction of travel
            if self.pos != self.prevPos:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos, True

        return super().getNextPos(game)
