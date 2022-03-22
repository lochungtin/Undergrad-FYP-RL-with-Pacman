from time import sleep
from typing import List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from utils.coordinate import CPair
from utils.grid import createGameSizeGrid

class Solver:
    DEFAULT_CONFIG = {
        "maxIter": 10000,
        "gamma": 0.90,
        "epsilon": 0.00005,
    }

    def __init__(self, game: "Game", rewards: dict[str, float], config: dict[str, object] = DEFAULT_CONFIG) -> None:
        # game
        self.game: Game = game

        # reward values
        self.rewards: dict[str, float] = rewards

        # hyperparameters
        self.gamma: float = config["gamma"]
        self.epsilon: float = config["epsilon"]

        # max iteration count
        self.maxIter: int = config["maxIter"]

    # get optimal action
    def getAction(self, pos: CPair) -> int:
        # get reward grid
        rewardGrid: List[List[float]] = self.makeRewardGrid()

        # perform value iteration
        utilities: List[List[float]] = createGameSizeGrid(0)
        for i in range(self.maxIter):
            utilities, stable = self.bellmanUpdate(utilities, rewardGrid)

            if stable:
                break

        # get optimal action
        return np.argmax(self.getUtilValues(utilities, pos))

    # bellman update for value iterations
    def bellmanUpdate(
        self,
        utilities: List[List[float]],
        rewards: List[List[float]],
    ) -> Tuple[List[List[float]], bool]:
        # initialise new utility value grid
        newUtils: List[List[float]] = createGameSizeGrid(0)

        # stable indicator
        stable = True

        # get new utility values
        for i, row in enumerate(self.game.state):
            for j, cell in enumerate(row):
                if not cell.isWall:
                    newUtils[i][j] = rewards[i][j] + self.gamma * max(self.getUtilValues(utilities, cell.coords))

                    if abs(newUtils[i][j] - utilities[i][j]) > self.epsilon:
                        stable = False

        return newUtils, stable

    # get utility value of neighbours
    def getUtilValues(self, utilities: List[List[float]], pos: CPair):
        adjVals: List[float] = [float("-inf"), float("-inf"), float("-inf"), float("-inf")]

        for action, neighbour in self.game.getCell(pos).adj.items():
            if not neighbour is None:
                adjVals[action] = utilities[neighbour.coords.row][neighbour.coords.col]

        return adjVals

    # ===== TO BE OVERRIDDEN =====
    def makeRewardGrid(self) -> List[List[float]]:
        raise NotImplementedError()
