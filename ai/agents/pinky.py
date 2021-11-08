from ai.agents.agent import Agent
from ai.predictable import Predictable
from data import POS, REP


class BlinkyAI(Agent):
    def __init__(self, predictable: Predictable) -> None:
        super().__init__(POS.PINKY, REP.PINKY, predictable)
