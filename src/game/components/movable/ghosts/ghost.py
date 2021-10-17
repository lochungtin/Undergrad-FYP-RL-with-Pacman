from typing import Tuple

from data import GHOST_MODE
from game.components.movable.movable import Movable
from utils.coordinate import CPair


class Ghost(Movable):
    def __init__(self, pos: CPair, repId: int) -> None:
        super().__init__(pos, repId)

        self.mode: int = GHOST_MODE.CHASE
        self.steps = 200

    def getTargetTile(self) -> CPair:
        return CPair(0, 0)

    def getNextPos(self) -> Tuple[CPair, CPair]:
        return super().getNextPos()

    def setMode(self, mode: int, steps: int) -> None:
        self.mode = mode
        self.steps = steps
