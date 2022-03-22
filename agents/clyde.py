from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.ghost import ClassicGhostAgent, StaticGhostAgent
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair


# original agent for clyde
class ClydeClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        ClassicGhostAgent.__init__(self, POS.CLYDE, REP.CLYDE, GHOST_MODE.GHOST_EXIT_INTERVAL * 2)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # scatter mode (head to corner)
        if self.mode == GHOST_MODE.SCATTER:
            return POS.CLYDE_CORNER

        # chase mode
        if self.pos != game.pacman.pos:
            if len(self.pathfinder.start(self.pos, game.pacman.pos, self.direction)) < 4:
                return POS.CLYDE_CORNER

        return game.pacman.pos


# hyperaggressive agent for clyde
class ClydeClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        ClassicGhostAgent.__init__(self, POS.CLYDE, REP.CLYDE, GHOST_MODE.GHOST_EXIT_INTERVAL * 2)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # chase mode
        if self.pos != game.pacman.pos:
            if len(self.pathfinder.start(self.pos, game.pacman.pos, self.direction)) < 4:
                return POS.CLYDE_CORNER

        return game.pacman.pos


# static agent for clyde
class ClydeStaticAgent(StaticGhostAgent):
    def __init__(self) -> None:
        StaticGhostAgent.__init__(self, POS.CLYDE, REP.CLYDE)
