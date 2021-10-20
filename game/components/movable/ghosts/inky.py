from typing import List

from data import DATA, DIR, GHOST_MODE, POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.components.movable.pacman import Pacman
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Inky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.INKY, REP.INKY, DATA.GHOST_EXIT_INTERVAL * 1, pathfinder)

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
            return POS.INKY_CORNER
            
        # chase mode
        # get reflection tile
        pivot: CPair = pacman.pos
        for _ in range(4):
            pivot = pivot.move(pacman.direction)

        # replicate target tile bug in classic pacman
        if pacman.direction == DIR.UP:
            for _ in range(4):
                pivot = pivot.move(DIR.LF)

        # reflect blinky's position wrt to reflection tile to get target tile
        return blinkyPos.reflect(pivot)
