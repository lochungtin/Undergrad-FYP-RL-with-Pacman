from typing import List, Tuple

from data import GHOST_MODE, POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Blinky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, False, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        # cruise elroy mode
        if self.mode == GHOST_MODE.CRUISE_ELROY:
            return super().getPacmanPos(state)

        # frightened mode (ignore)
        elif self.isFrightened:
            return None

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            if self.pos == POS.BLINKY_CORNER:
                return self.prevPos
            else:
                return POS.BLINKY_CORNER
            
        # chase mode
        return super().getPacmanPos(state)
