from typing import List, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

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
    def processGameState(self, game: "Game") -> List[int]:
        rt: List[int] = []

        for row in game.state:
            for cell in row:
                if cell == REP.BLINKY:
                    rt.append(6 + game.blinky.isFrightened * 4)
                elif cell == REP.INKY:
                    rt.append(6 + game.inky.isFrightened * 4)
                elif cell == REP.CLYDE:
                    rt.append(6 + game.clyde.isFrightened * 4)
                elif cell == REP.PINKY:
                    rt.append(6 + game.pinky.isFrightened * 4)
                else:
                    rt.append(cell)

        return rt
