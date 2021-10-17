from typing import Tuple

from data import REP
from game.components.movable.ghosts.ghost import Ghost
from utils.coordinate import CPair


class Blinky(Ghost):
    def __init__(self, pos: CPair) -> None:
        super().__init__(pos, REP.BLINKY)

    # get target tile of ghost
    def getTargetTile(self) -> CPair:
        return super().getTargetTile()
