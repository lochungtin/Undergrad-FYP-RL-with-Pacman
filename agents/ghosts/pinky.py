from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent
from data.data import DIR, GHOST_MODE, POS, REP
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


# classic ai agent for pinky
class PinkyClassicAgent(ClassicGhostAgent):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(self, POS.PINKY, REP.PINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.PINKY_CORNER

        # chase mode
        targetTile: CPair = game.pacman.pos
        for _ in range(4):
            targetTile = targetTile.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(4):
                targetTile = targetTile.move(DIR.LF)

        return targetTile


# classic aggressive ai agent for pinky
class PinkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self, pf: PathFinder) -> None:
        super().__init__(self, POS.PINKY, REP.PINKY, 0, pf)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # chase mode
        targetTile: CPair = game.pacman.pos
        for _ in range(4):
            targetTile = targetTile.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(4):
                targetTile = targetTile.move(DIR.LF)

        return targetTile
