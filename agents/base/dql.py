from typing import List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from agents.base.agent import DirectionAgent
from ai.deepq.neuralnet import NeuralNet
from utils.coordinate import CPair


# base class for all (pacman and ghosts) deep q learning based agents
class DQLAgent(DirectionAgent):
    def __init__(self, pos: CPair, repId: int, neuralNet: NeuralNet) -> None:
        DirectionAgent.__init__(self, pos, repId)

        self.neuralNet: NeuralNet = neuralNet

    # get next position of agent
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # selection optimal direction
        self.setDir(
            # select optimal action
            np.argmax(
                # get q values
                self.neuralNet.predict(
                    # parse game state to feature vector
                    np.array([self.processGameState(game)]),
                )
            )
        )
        return super().getNextPos(game)

    # ===== REQUIRED TO OVERRIDE =====
    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[float]:
        raise NotImplementedError
