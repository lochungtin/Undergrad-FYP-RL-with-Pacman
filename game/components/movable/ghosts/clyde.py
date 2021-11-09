from typing import List

from data.data import DATA, GHOST_MODE, POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.components.movable.pacman import Pacman
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Clyde(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.CLYDE, REP.CLYDE, DATA.GHOST_EXIT_INTERVAL * 2, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, pacman: Pacman, blinkyPos: CPair) -> CPair:
        # frightened mode (ignore)
        if self.isFrightened:
            return None

        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.CLYDE_CORNER

        # chase mode
        if len(self.pathfinder.start(self.pos, pacman.pos, self.direction).path) < 8:
            return POS.CLYDE_CORNER

        return pacman.pos
