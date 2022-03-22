from copy import deepcopy
from random import Random
from typing import List, Tuple, TYPE_CHECKING
import numpy as np


if TYPE_CHECKING:
    from game.game import Game

from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from agents.base.base import DirectionAgent
from data.config import BOARD, POS
from data.data import GHOST_MODE
from game.components.component import Component
from game.utils.cell import Cell
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair
from utils.direction import DIR

# base class for all ghost neuro-evolution based agents
class NEATAgent(DirectionAgent):
    def __init__(self, pos: CPair, repId: int, genome: Genome) -> None:
        DirectionAgent.__init__(self, pos, repId)

        self.genome: Genome = genome

    # get next position of ghost
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # get action vals
        state: List[int] = self.processGameState(game.state)
        qVals: List[float] = self.genome.predict(self.processGameState(state))

        # get optimal action
        action: int = np.argmax(qVals)

        # selection action direction
        self.setDir(action)

        return DirectionAgent().getNextPos(game)

    # ===== REQUIRED TO OVERRIDE =====
    # preprocess game state for neural network
    def processGameState(self, state: List[List[int]]) -> List[int]:
        raise NotImplementedError
