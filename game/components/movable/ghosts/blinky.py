from typing import List, Tuple

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
        # frightened mode (ignore)
        if self.isFrightened:
            return None

        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
            return POS.BLINKY_CORNER

        # chase mode
        return pacman.pos

    # get next postition of blinky (overrided for cruise elroy mode)
    def getNextPos(
        self, state: List[List[int]], pacman: Pacman, blinkyPos: CPair
    ) -> Tuple[CPair, CPair]:

        if self.mode == GHOST_MODE.CRUISE_ELROY:
            # generate path
            self.prevPath = self.path
            self.path = self.pathfinder.start(self.pos, pacman.pos, self.direction)

            self.prevPos = self.pos
            self.pos = self.path.path[0]

            # update direction of travel
            if self.pos != self.prevPos:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos

        return super().getNextPos(state, pacman, blinkyPos)
