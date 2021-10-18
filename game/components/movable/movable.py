from typing import List, Tuple

from game.components.component import Component
from utils.coordinate import CPair


class Movable(Component):
    def __init__(self, pos: CPair, repId: int) -> None:
        super().__init__(pos, repId)

        self.prevPos: CPair = pos

    # get next position of character
    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        return self.pos, self.prevPos
