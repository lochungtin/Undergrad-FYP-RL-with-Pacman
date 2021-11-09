from ai.agents.agent import Agent
from ai.predictable import Predictable
from data.data import POS, REP


class BlinkyAI(Agent):
    def __init__(self, predictable: Predictable) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, predictable)
