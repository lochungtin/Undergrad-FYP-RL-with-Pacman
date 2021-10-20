from typing import List

from data import DIR, GHOST_MODE, POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.components.movable.pacman import Pacman
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Pinky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.PINKY, REP.PINKY, 0, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, pacman: Pacman, blinkyPos: CPair) -> CPair:
        # frightened mode (ignore)
        if self.isFrightened:
            return None

        # dead
        if self.dead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.PINKY_CORNER
            
        # chase mode
        targetTile: CPair = pacman.pos
        for _ in range(4):
            targetTile = targetTile.move(pacman.direction)

        # replicate target tile bug in classic pacman
        if pacman.direction == DIR.UP:
            for _ in range(4):
                targetTile = targetTile.move(DIR.LF)

        return targetTile
