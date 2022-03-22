from math import log2
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.agent import DirectionAgent
from agents.base.dql import DQLAgent
from agents.base.mdp import MDPAgent
from agents.utils.features import pacmanFeatureExtraction
from ai.deepq.neuralnet import NeuralNet
from ai.mdp.solver import Solver
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from utils.grid import createGameSizeGrid


# playable keyboard agent for pacman
class PlayableAgent(DirectionAgent):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


# mdp agent for pacman
class PacmanMDPSolver(Solver):
    def __init__(self, game: "Game", rewards: dict[str, float]) -> None:
        super().__init__(game, rewards)

    # set rewards
    def makeRewardGrid(self) -> List[List[float]]:
        # iniialise reward grid
        rewardGrid: List[List[float]] = createGameSizeGrid(self.rewards["timestep"])

        # set power pellet reward
        for key, pwrplt in self.game.pwrplts.items():
            if pwrplt.valid:
                avgGhostDist: float = 1
                for ghost in self.game.ghostList:
                    if not ghost.isDead:
                        avgGhostDist += pwrplt.pos.manDist(ghost.pos)

                avgGhostDist /= len(self.game.ghostList)

                rewardGrid[pwrplt.pos.row][pwrplt.pos.col] = self.rewards["pwrplt"] * (1 / avgGhostDist**2)

        # set pellet reward
        for key, pellet in self.game.pellets.items():
            if pellet.valid:
                rewardGrid[pellet.pos.row][pellet.pos.col] = self.rewards["pellet"] * log2(
                    BOARD.TOTAL_PELLET_COUNT - self.game.pelletProgress + 1
                )

        # set ghost reward
        for ghost in self.game.ghostList:
            if not ghost.isDead:
                if ghost.isFrightened:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = (
                        self.rewards["kill"] * self.game.pwrpltEffectCounter / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT
                    )
                else:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = self.rewards["ghost"]

        return rewardGrid


class PacmanMDPAgent(MDPAgent):
    def __init__(self) -> None:
        MDPAgent.__init__(
            self,
            POS.PACMAN,
            REP.PACMAN,
            PacmanMDPSolver,
            {
                "timestep": -0.5,
                "pwrplt": 3,
                "pellet": 10,
                "kill": 50,
                "ghost": -100,
            },
        )


# deep q learning training agent for pacman
class PacmanDQLTAgent(DirectionAgent):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


# deep q learning agent for pacman
class PacmanDQLAgent(DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return pacmanFeatureExtraction(game)
