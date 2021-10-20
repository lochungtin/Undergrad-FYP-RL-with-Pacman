from typing import List

from data import GHOST_MODE, POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Pinky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.PINKY, REP.PINKY, 0, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        # frightened mode (ignore)
        if self.isFrightened:
            return None

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.PINKY_CORNER
            
        # chase mode
        return super().getPacmanPos(state)
