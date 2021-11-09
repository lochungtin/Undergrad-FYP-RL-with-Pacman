from random import randint
from typing import List

from ai.agents.agent import Agent
from ai.predictable import Predictable
from data.data import POS, REP


class PacmanAI(Agent):
    def __init__(self, predictable: Predictable) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, predictable)

    def processState(self, state: List[List[int]]) -> List[int]:
        input = []
        for i in range(10):
            input.append(randint(1, 10))

        return input
