from typing import List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from agents.base.agent import DirectionAgent
from ai.neat.genome import Genome
from utils.coordinate import CPair


# base class for all neuroevolution based agents
class NEATAgent(DirectionAgent):
    def __init__(self, pos: CPair, repId: int, genome: Genome) -> None:
        DirectionAgent.__init__(self, pos, repId)

        self.genome: Genome = genome

    # get next position of ghost
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # selection optimal direction
        self.setDir(
            # select optimal action
            np.argmax(
                # get q values
                self.genome.predict(
                    # parse game state to feature vector
                    self.processGameState(game),
                )
            )
        )
        return DirectionAgent.getNextPos(self, game)

    # ===== REQUIRED TO OVERRIDE =====
    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        raise NotImplementedError
