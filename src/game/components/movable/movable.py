from typing import Tuple

from game.components.component import Component
from utils.coordinate import CPair


class Movable(Component):
    def __init__(self, pos: CPair, repId: int) -> None:
        super().__init__(pos, repId)

        self.prevPos: CPair = pos

    def getNextPos(self) -> Tuple[CPair, CPair]:
        return self.pos, self.prevPos
