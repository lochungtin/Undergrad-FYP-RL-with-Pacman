from ai.agents.agent import Agent
from ai.predictable import Predictable
from data.data import POS, REP


class ClydeAI(Agent):
    def __init__(self, predictable: Predictable) -> None:
        super().__init__(POS.CLYDE, REP.CLYDE, predictable)
