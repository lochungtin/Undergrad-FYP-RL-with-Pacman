from typing import List, Tuple
from ai.agents.predictable import Predictable
from data import REP

from game.components.movable.movable import Movable
from utils.coordinate import CPair


class Agent(Movable):
    def __init__(self, pos: CPair, repId: int, predictable: Predictable) -> None:
        super().__init__(pos, repId)

        self.predictable: Predictable = predictable

    def processState(state: List[List[int]]) -> List[int]:
        return []

    def getNextPos(self, state: List[List[int]]) -> Tuple[CPair, CPair]:
        actionValues: List[float] = self.predictable.predict(self.processState(state))
        index: int = -1
        value: float = float('-inf')
        for i, val in enumerate(actionValues):
            if val > value:
                index = i
                value = val

        self.moved = False

        newPos: CPair = self.pos.move(i)
        if newPos.isValid() and not REP.isWall(state[newPos.row][newPos.col]):
            self.prevPos = self.pos
            self.pos = newPos
            self.moved = True

        return self.pos, self.prevPos
