from typing import List

from ai.deepq.neuralnet import NeuralNet
from agents.base import DQLAgent, DirectionAgent
from data.data import POS, REP


# playable keyboard agent for pacman
class PlayableAgent(DirectionAgent):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


# deep q learning agent for pacman
class PacmanDQLAgent(DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, state: List[List[int]]) -> List[int]:
        rt: List[int] = []

        for row in state:
            for cell in row:
                if REP.isGhost(cell):
                    rt.append(6)
                else:
                    rt.append(cell)

        return rt
