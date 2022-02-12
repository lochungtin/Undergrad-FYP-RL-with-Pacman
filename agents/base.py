from copy import deepcopy
from random import randint, random, choice
from typing import List, Tuple

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from ai.predictable import Predictable
from data.data import DIR, REP
from game.components.component import Component
from utils.coordinate import CPair


# base class for game agents (pacman and ghosts)
class Base(Component):
    def __init__(self, pos: CPair, repId: int) -> None:
        super().__init__(pos, repId)

        self.direction: int = DIR.UP
        self.prevPos: CPair = deepcopy(pos)

        self.moved: bool = True

    # get next position of character
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair]:
        raise NotImplementedError


# base class for intelligent agents (pacman and ghosts)
class IntelligentBase(Base):
    def __init__(
        self,
        pos: CPair,
        repId: int,
        predictable: Predictable,
        undeterministic: float = -1,
    ) -> None:
        super().__init__(pos, repId)

        self.predictable: Predictable = predictable
        self.undeterministic: float = undeterministic

    # process the state into neural network input
    def processState(self, game: "Game") -> List[int]:
        raise NotImplementedError

    # get next position of agent
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair]:
        # action index
        index: int = 0

        if self.undeterministic > 1 - random():
            # explore
            index = randint(0, 3)
        else:
            # predict action values
            actionValues: List[float] = self.predictable.predict(self.processState(game))

            # select optimal valid action
            actionIdx: List[Tuple[int, float]] = sorted(
                [(i, val) for i, val in enumerate(actionValues)],
                key=lambda p: p[1],
                reverse=True,
            )

            for i, p in enumerate(actionIdx):
                newPos: CPair = self.pos.move(p[0])
                if newPos.isValid() and not REP.isWall(game.state[newPos.row][newPos.col]):
                    index = p[0]
                    break

            # print(actionIdx, index, i)

            if hasattr(game, "invalidSteps"):
                game.invalidSteps += i

        # update positions
        self.moved = False

        newPos: CPair = self.pos.move(index)
        if newPos.isValid() and not REP.isWall(game.state[newPos.row][newPos.col]):
            self.prevPos = self.pos
            self.pos = newPos
            self.moved = True

        return self.pos, self.prevPos
