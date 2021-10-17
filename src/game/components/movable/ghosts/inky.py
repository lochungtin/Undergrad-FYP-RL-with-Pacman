from typing import Tuple

from data import REP
from game.components.movable.ghosts.ghost import Ghost
from utils.coordinate import CPair


class Inky(Ghost):
    def __init__(self, pos: CPair) -> None:
        super().__init__(pos, REP.INKY)

    def getNextPos(self) -> Tuple[CPair, CPair]:
        return super().getNextPos()
