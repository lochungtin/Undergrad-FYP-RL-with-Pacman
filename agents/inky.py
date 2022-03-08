from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair
from utils.direction import DIR

# classic ai agent for inky
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


# classic aggressive ai agent for inky
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
