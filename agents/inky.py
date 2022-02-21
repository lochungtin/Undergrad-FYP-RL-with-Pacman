from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent
from data.config import POS
from data.data import DATA, GHOST_MODE, REP
from utils.coordinate import CPair
from utils.direction import DIR

# classic ai agent for inky
class InkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.INKY, REP.INKY, DATA.GHOST_EXIT_INTERVAL)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.INKY_CORNER

        # chase mode
        # get reflection tile
        pivot: CPair = game.pacman.pos
        for _ in range(4):
            pivot = pivot.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(4):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return game.blinky.pos.reflect(pivot)


# classic aggressive ai agent for inky
class InkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.INKY, REP.INKY, DATA.GHOST_EXIT_INTERVAL)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        # get reflection tile
        pivot: CPair = game.pacman.pos
        for _ in range(4):
            pivot = pivot.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(4):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return game.blinky.pos.reflect(pivot)
