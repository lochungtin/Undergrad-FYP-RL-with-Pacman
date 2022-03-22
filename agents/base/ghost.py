from random import Random
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.base import GhostAgent
from agents.base.dql import DQLAgent
from agents.base.mdp import MDPAgent
from agents.utils.features import ghostFeatureExtraction
from ai.deepq.neuralnet import NeuralNet
from ai.mdp.solver import Solver
from data.config import POS
from data.data import GHOST_MODE, REP
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR
from utils.grid import createGameSizeGrid


# base class for classic ghost agents
class ClassicGhostAgent(GhostAgent):
    def __init__(self, pos: CPair, repId: int, initWait: int) -> None:
        GhostAgent.__init__(self, pos, repId)

        # ghost mode
        self.mode: int = GHOST_MODE.SCATTER

        # initial waiting countdown
        self.initWait: int = initWait

        # random state (for set seed analysis)
        self.rand: Random = Random()

    # get regular movement positions
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # start random walk if frightened
        if self.isFrightened and (not hasattr(self, "cruiseElroy") or not self.cruiseElroy):
            # slow down ghost speed
            self.speedReducer = (self.speedReducer + 1) % GHOST_MODE.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE
            if self.speedReducer == 0:
                # filter out valid locations
                valid: List[Cell] = []
                for dir, neighbour in game.state[self.pos.row][self.pos.col].adj.items():
                    if not neighbour is None and not (dir != DIR.UP and self.pos in POS.GHOST_NO_UP_CELLS):
                        valid.append(neighbour)

                # random choice
                self.prevPos = self.pos
                self.pos = self.rand.choice(valid).coords
                self.moved = True

        # regular behaviour
        else:
            # get target tile
            targetTile: CPair = self.getTargetTile(game)

            # looping mechanic
            if self.pos == targetTile:
                targetTile = self.prevPos

            # generate path
            self.prevPath = self.path
            if self.pos != targetTile:
                self.path = self.pathfinder.start(self.pos, targetTile, self.direction)

            # update positions
            self.prevPos = self.pos
            if len(self.path) > 0:
                self.pos = self.path[0]
            self.moved = True

        # update direction of travel
        if self.moved:
            self.direction = self.pos.relate(self.prevPos)

        return self.pos, self.prevPos, self.moved

    # ===== REQUIRED TO OVERRIDE =====
    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        raise NotImplementedError


# base mdp solver for mdp based ghost agnets
class GhostMDPSolver(Solver):
    def __init__(self, game: "Game", rewards: dict[str, float], gId: int) -> None:
        super().__init__(game, rewards)

        # ghost id
        self.gId: int = gId

    # set rewards
    def makeRewardGrid(self) -> List[List[float]]:
        rewardGrid: List[List[float]] = createGameSizeGrid(self.rewards["timestep"])

        # set pacman reward
        pPos: CPair = self.game.pacman.pos

        pacmanReward: float = self.rewards["pacmanR"]
        if self.game.ghosts[self.gId].isFrightened:
            pacmanReward = self.rewards["pacmanF"]
        rewardGrid[pPos.row][pPos.col] = pacmanReward

        # set ghost neighbour reward
        for ghost in self.game.ghostList:
            if ghost.repId != self.gId:
                if not ghost.isDead:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = self.rewards["ghost"]

        return rewardGrid


# base class for mdp based ghost agents
class MDPGhostAgent(GhostAgent, MDPAgent):
    REWARDS = {
        "ghost": 5,
        "pacmanR": 20,
        "pacmanF": -10,
        "timestep": -0.5,
    }

    def __init__(
        self,
        pos: CPair,
        repId: int,
        solver: type,
        rewards: dict[str, float] = REWARDS,
    ) -> None:
        GhostAgent.__init__(self, pos, repId)
        MDPAgent.__init__(self, pos, repId, solver, rewards)

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return MDPAgent.getNextPos(self, game)


# base class for deep q learning based ghost agnets
class DQLGhostAgent(GhostAgent, DQLAgent):
    def __init__(self, pos: CPair, repId: int, neuralNet: NeuralNet) -> None:
        GhostAgent.__init__(self, pos, repId)
        DQLAgent.__init__(self, pos, repId, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return ghostFeatureExtraction(game, self.repId)

    # get regular movement (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return DQLAgent.getNextPos(self, game)


# placeholder ghost agent
class StaticGhostAgent(GhostAgent):
    def __init__(self, pos: CPair, repId: int) -> None:
        GhostAgent.__init__(self, pos, repId)

        self.moved = False

    # return static position
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return self.pos, self.pos, False
