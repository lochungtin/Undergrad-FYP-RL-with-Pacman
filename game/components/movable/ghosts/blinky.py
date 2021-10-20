from typing import List

from data import GHOST_MODE, POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.components.movable.pacman import Pacman
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Blinky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, pacman: Pacman, blinkyPos: CPair) -> CPair:
        # cruise elroy mode
        if self.mode == GHOST_MODE.CRUISE_ELROY:
            return pacman.pos

        # frightened mode (ignore)
        elif self.isFrightened:
            return None

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.BLINKY_CORNER
            
        # chase mode
        return pacman.pos
