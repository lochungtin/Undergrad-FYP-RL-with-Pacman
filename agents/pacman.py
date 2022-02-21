from typing import List, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from ai.deepq.neuralnet import NeuralNet
from agents.base import DQLAgent, DirectionAgent
from data.config import POS
from data.data import REP


def pacmanFeatureExtraction(game: "Game") -> List[int]:
    pass

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
        return pacmanFeatureExtraction(game)