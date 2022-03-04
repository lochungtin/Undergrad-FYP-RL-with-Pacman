from math import log2
from queue import Queue
from typing import List, TYPE_CHECKING, Tuple

import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from ai.deepq.neuralnet import NeuralNet
from agents.base import DQLAgent, DirectionAgent, GhostAgent
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.grid import createGameSizeGrid


def distanceComparison(ref: CPair, comp: CPair) -> List[float]:
    return [
        max(0, ref.row - comp.row) / BOARD.ROW,
        max(0, comp.row - ref.row) / BOARD.ROW,
        max(0, ref.col - comp.col) / BOARD.COL,
        max(0, comp.col - ref.col) / BOARD.COL,
    ]


def pacmanFeatureExtraction(game: "Game") -> List[float]:
    features: List[float] = [0, 0, 0, 0, (game.pwrpltEffectCounter + 1) / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT]

    pPos: CPair = game.pacman.pos
    pCell: Cell = game.getCell(pPos)

    # feature 1: valid directions
    for action, neighbour in pCell.adj.items():
        if not neighbour is None:
            features[action] = 1

    # feature 2: relative position to closest pellet
    closestPellet: CPair = 0

    openlist: Queue[Cell] = Queue()
    openlist.put(pCell)
    closedList: List[List[bool]] = createGameSizeGrid(False)

    while not openlist.empty():
        # get current visiting cell
        curCell = openlist.get()

        # update closed list
        closedList[curCell.coords.row][curCell.coords.col] = True

        if curCell.hasPellet:
            closestPellet = curCell.coords
            break

        for neighbour in curCell.getValidNeighbours():
            if not closedList[neighbour.coords.row][neighbour.coords.col]:
                openlist.put(neighbour)

    features += distanceComparison(pPos, closestPellet)

    # feature 3: relative position to closest power pellet
    closestPwrplt: CPair = pPos
    closestPwrpltD: int = BOARD.MAX_DIST
    for key, pwrplt in game.pwrplts.items():
        if pwrplt.valid:
            d: int = pPos.manDist(pwrplt.pos)
            if d < closestPwrpltD:
                closestPwrplt = pwrplt.pos
                closestPwrpltD = d

    features += distanceComparison(pPos, closestPwrplt)

    # feature 4: relative position to #1 closest ghost + ghost state
    g0: GhostAgent = game.ghostList[0]
    if g0.isDead:
        features += [0, 0, 0, 0, 0]
    else:
        features += distanceComparison(pPos, g0.pos)
        features.append(g0.isFrightened * 1)

    # feature 5: relative position to #2 closest ghost + ghost state
    g1: GhostAgent = game.ghostList[1]
    if g1.isDead:
        features += [0, 0, 0, 0, 0]
    else:
        features += distanceComparison(pPos, g1.pos)
        features.append(g1.isFrightened * 1)

    return features


# playable keyboard agent for pacman
class PlayableAgent(DirectionAgent):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


# mdp agent for pacman
class PacmanMDPAgent(DirectionAgent):
    def __init__(self, rewards: dict[str, float], gamma: float, epsilon: float, maxIter: int) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)

        self.rewards: dict[str, float] = rewards

        self.gamma: float = gamma
        self.epsilon: float = epsilon

        self.maxIter: int = maxIter

    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.setDir(self.mdpGetAction(game))
        return super().getNextPos(game)

    # ===== mdp solving functions =====
    def mdpGetAction(self, game: "Game") -> int:
        # get reward grid
        rewardGrid: List[List[float]] = self.makeRewardGrid(game)

        # perform value iteration
        utilities: List[List[float]] = createGameSizeGrid(0)
        for i in range(self.maxIter):
            utilities, stable = self.bellmanUpdate(utilities, rewardGrid, game)

            if stable:
                break

        # get optimal action
        return np.argmax(self.getUtilValues(utilities, game, game.pacman.pos))

    # create reward grid from state space
    def makeRewardGrid(self, game: "Game",) -> List[List[float]]:
        # iniialise reward grid
        rewardGrid: List[List[float]] = createGameSizeGrid(self.rewards["timestep"])

        # set power pellet reward
        for key, pwrplt in game.pwrplts.items():
            if pwrplt.valid:
                avgGhostDist: float = 1
                for ghost in game.ghostList:
                    if not ghost.isDead:
                        avgGhostDist += pwrplt.pos.manDist(ghost.pos)

                avgGhostDist /= len(game.ghostList)

                rewardGrid[pwrplt.pos.row][pwrplt.pos.col] = self.rewards["pwrplt"] * (1 / avgGhostDist**2)

        # set pellet reward
        for key, pellet in game.pellets.items():
            if pellet.valid:
                rewardGrid[pellet.pos.row][pellet.pos.col] = self.rewards["pellet"] * log2(
                    BOARD.TOTAL_PELLET_COUNT - game.pelletProgress + 1
                )

        # set ghost reward
        for ghost in game.ghostList:
            if not ghost.isDead:
                if ghost.isFrightened:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = (
                        self.rewards["kill"] * game.pwrpltEffectCounter / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT
                    )
                else:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = self.rewards["ghost"]

        return rewardGrid

    # bellman update for value iterations
    def bellmanUpdate(
        self,
        utilities: List[List[float]],
        rewards: List[List[float]],
        game: "Game",
    ) -> Tuple[List[List[float]], bool]:
        # initialise new utility value grid
        newUtils: List[List[float]] = createGameSizeGrid(0)

        # stable indicator
        stable = True

        # get new utility values
        for i, row in enumerate(game.state):
            for j, cell in enumerate(row):
                if not cell.isWall:
                    newUtils[i][j] = rewards[i][j] + self.gamma * max(self.getUtilValues(utilities, game, cell.coords))

                    if abs(newUtils[i][j] - utilities[i][j]) > self.epsilon:
                        stable = False

        return newUtils, stable

    # get utility value of neighbours
    def getUtilValues(self, utilities: List[List[float]], game: "Game", pos: CPair):
        adjVals: List[float] = [float("-inf"), float("-inf"), float("-inf"), float("-inf")]

        for action, neighbour in game.getCell(pos).adj.items():
            if not neighbour is None:
                adjVals[action] = utilities[neighbour.coords.row][neighbour.coords.col]

        return adjVals


# deep q learning agent for pacman
class PacmanDQLAgent(DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return pacmanFeatureExtraction(game)
