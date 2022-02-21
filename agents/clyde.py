from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent
from data.config import POS
from data.data import DATA, GHOST_MODE, REP
from utils.coordinate import CPair


# classic ai agent for clyde
class ClydeClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.CLYDE, REP.CLYDE, DATA.GHOST_EXIT_INTERVAL * 2)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.CLYDE_CORNER

        # chase mode
        if self.pos != game.pacman.pos:
            if len(self.pathfinder.start(self.pos, game.pacman.pos, self.direction).path) < 8:
                return POS.CLYDE_CORNER

        return game.pacman.pos


# classic aggressive ai for clyde
class ClydeClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.CLYDE, REP.CLYDE, DATA.GHOST_EXIT_INTERVAL * 2)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        if self.pos != game.pacman.pos:
            if len(self.pathfinder.start(self.pos, game.pacman.pos, self.direction).path) < 8:
                return POS.CLYDE_CORNER

        return game.pacman.pos
