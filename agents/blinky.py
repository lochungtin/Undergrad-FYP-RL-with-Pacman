from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.base import DirectionAgent, GhostAgent
from agents.base.dql import DQLAgent
from agents.base.ghost import ClassicGhostAgent
from agents.utils.features import ghostFeatureExtraction
from ai.deepq.neuralnet import NeuralNet
from ai.mdp.solver import Solver
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair
from utils.grid import createGameSizeGrid


# classic ai agent for blinky
class BlinkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        ClassicGhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, 0)

        self.cruiseElroy: bool = False

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # scatter mode (head to corner)
        if self.mode == GHOST_MODE.SCATTER:
            return POS.BLINKY_CORNER

        # chase mode
        return game.pacman.pos


# classic aggressive ai agent for blinky
class BlinkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        ClassicGhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, 0)

        self.cruiseElroy: bool = False

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # chase mode
        return game.pacman.pos


# mdp agent for blinky
class BlinkyMDPSolver(Solver):
    def __init__(self, game: "Game", rewards: dict[str, float]) -> None:
        super().__init__(game, rewards)

    # set rewards
    def makeRewardGrid(self) -> List[List[float]]:
        rewardGrid: List[List[float]] = createGameSizeGrid(self.rewards["timestep"])

        # set pacman reward
        pPos: CPair = self.game.pacman.pos
        pacmanReward: float = self.rewards["pacmanR"]
        if self.game.ghosts[REP.BLINKY].isFrightened:
            pacmanReward = self.rewards["pacmanF"]
        rewardGrid[pPos.row][pPos.col] = pacmanReward

        # set ghost neighbour reward
        for ghost in self.game.ghostList:
            if ghost.repId != REP.BLINKY:
                if not ghost.isDead:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = self.rewards["ghost"]

        return rewardGrid


class BlinkyMDPAgent(GhostAgent, DirectionAgent):
    def __init__(self) -> None:
        GhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, False)
        DirectionAgent.__init__(self, POS.BLINKY, REP.BLINKY)

        # reward values
        self.rewards: dict[str, float] = {
            "ghost": 0,
            "pacmanF": -10,
            "pacmanR": 20,
            "timestep": -0.05,
        }

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.setDir(BlinkyMDPSolver(game, self.rewards).getAction(self.pos))
        return DirectionAgent.getNextPos(self, game)


# deep q learning training agent for blinky
class BlinkyDQLTAgent(GhostAgent, DirectionAgent):
    def __init__(self) -> None:
        GhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, False)
        DirectionAgent.__init__(self, POS.BLINKY, REP.BLINKY)

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return DirectionAgent.getNextPos(self, game)


# deep q learning agent for pacman
class BlinkyDQLAgent(GhostAgent, DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        GhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, False)
        DQLAgent.__init__(self, POS.BLINKY, REP.BLINKY, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return ghostFeatureExtraction(game, self.repId)

    # get regular movement (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return DQLAgent.getNextPos(self, game)
