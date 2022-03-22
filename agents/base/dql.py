from typing import List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from agents.base.base import DirectionAgent
from ai.deepq.neuralnet import NeuralNet
from utils.coordinate import CPair

# base class for all (pacman and ghosts) deep q learning based agents
class DQLAgent(DirectionAgent):
    def __init__(self, pos: CPair, repId: int, neuralNet: NeuralNet) -> None:
        DirectionAgent.__init__(self, pos, repId)

        self.neuralNet: NeuralNet = neuralNet

    # get next position of agent
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # get action vals
        state: List[int] = self.processGameState(game)
        qVals: List[float] = self.neuralNet.predict(np.array([state]))

        # get optimal action
        action: int = np.argmax(qVals)

        # selection action direction
        self.setDir(action)

        return super().getNextPos(game)

    # ===== REQUIRED TO OVERRIDE =====
    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        raise NotImplementedError
