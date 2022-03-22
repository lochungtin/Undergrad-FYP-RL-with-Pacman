from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.ghost import ClassicGhostAgent, StaticGhostAgent
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair
from utils.direction import DIR

# original agent for inky
class InkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.INKY, REP.INKY, GHOST_MODE.GHOST_EXIT_INTERVAL)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # scatter mode (head to corner)
        if self.mode == GHOST_MODE.SCATTER:
            return POS.INKY_CORNER

        # chase mode
        # get reflection tile
        pivot: CPair = game.pacman.pos
        for _ in range(2):
            pivot = pivot.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(2):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return game.ghosts[REP.BLINKY].pos.reflect(pivot)


# hyperaggressive agent for inky
class InkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.INKY, REP.INKY, GHOST_MODE.GHOST_EXIT_INTERVAL)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # chase mode
        # get reflection tile
        pivot: CPair = game.pacman.pos
        for _ in range(2):
            pivot = pivot.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(2):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return game.ghosts[REP.BLINKY].pos.reflect(pivot)


# static agent for inky
class InkyStaticAgent(StaticGhostAgent):
    def __init__(self) -> None:
        StaticGhostAgent.__init__(self, POS.INKY, REP.INKY)
