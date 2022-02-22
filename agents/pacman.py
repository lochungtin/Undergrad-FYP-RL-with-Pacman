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


def bfs(starting: Cell, origin: Cell, game: "Game") -> List[float]:
    # targets: [pellet, power pellet, ghost, scared ghost, intersection]
    distances: List[int] = [0, 0, 0, 0, 0]
    completed: List[int] = [0, 0, 0, 0, 0]
    loc: List[Cell] = [None, None, None, None, None]

    openList: Queue[Tuple[int, Cell]] = Queue()
    openList.put((0, starting))

    closedList: List[List[bool]] = [[False for j in range(BOARD.COL)] for i in range(BOARD.ROW)]
    closedList[origin.coords.row][origin.coords.col] = True

    # premetively check power pellets and ghosts states to minimise computation
    # check if all power pellets are used
    allUsed: bool = True
    for id,  pwrplts in game.pwrplts.items():
        allUsed = allUsed and not pwrplts.valid

    if allUsed:
        completed[1] = True
        distances[1] = BOARD.MAX_DIST

    # check if all ghosts are dead or frightened
    allDead: bool = True
    allFrightened: bool = True
    allHostile: bool = True
    for ghost in game.ghostList:
        print(ghost.repId, ghost.isDead, ghost.isFrightened)
        allDead = allDead and ghost.isDead
        allHostile = allHostile and not ghost.isFrightened
        allFrightened = allFrightened and ghost.isFrightened
    print()

    if allDead:
        completed[2] = True
        completed[3] = True

        distances[2] = BOARD.MAX_DIST
        distances[3] = BOARD.MAX_DIST

    if allFrightened:
        completed[2] = True
        distances[2] = BOARD.MAX_DIST
    
    if allHostile:
        completed[3] = True
        distances[3] = BOARD.MAX_DIST

    while not openList.empty():
        data: Tuple[int, Cell] = openList.get()
        layer: int = data[0]
        curCell: Cell = data[1]

        # update closed list
        closedList[curCell.coords.row][curCell.coords.col] = True

        # check for intersections
        if curCell.isIntersection():
            completed[4] = 1
            loc[4] = curCell

        # check values
        if curCell.val != REP.EMPTY:
            if not completed[0] and curCell.val == REP.PELLET:
                completed[0] = 1
                loc[0] = curCell
            elif not completed[1] and curCell.val == REP.PWRPLT:
                completed[1] = 1
                loc[1] = curCell
            elif REP.isGhost(curCell.val):
                ghost: GhostAgent = game.ghosts[curCell.val]
                if not completed[2] and not ghost.isDead:
                    completed[2] = 1
                    loc[2] = curCell
                elif not completed[3] and ghost.isFrightened:
                    completed[3] = 1
                    loc[3] = curCell

        # check if all targets are found
        allDone: int = 1
        for i in range(5):
            allDone *= completed[i]

            if not completed[i]:
                distances[i] = layer + 1

        if allDone:
            break

        # add unvisited neighbours
        for neighbour in curCell.getValidNeighbours():
            if not closedList[neighbour.coords.row][neighbour.coords.col]:
                openList.put((layer + 1, neighbour))

    return list(zip(distances, loc))


def pacmanFeatureExtraction(game: "Game") -> List[float]:
    features: List[float] = []

    # feature 1: pellet progress
    features.append(game.pelletProgress / BOARD.TOTAL_PELLET_COUNT)

    # feature 2: vulnerability effect
    features.append(max(game.pwrpltEffectCounter, 0) / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT)

    # breadth first analysis
    pCell: Cell = game.getCell(game.pacman.pos)

    bfsRes: List[List[int]] = [None, None, None, None]
    curRes: List[int] = None
    for dir, neighbour in pCell.adj.items():
        if neighbour is None:
            if curRes is None:
                bfsRes[dir] = bfs(pCell, pCell, game)
            else:
                bfsRes[dir] = curRes
        else:
            bfsRes[dir] = bfs(neighbour, pCell, game)

    # feature 3: shortest distance to a pellet
    # feature 4: shortest distance to a power pellet
    # feature 5: shortest distance to a hostile ghost 
    # feature 6: shortest distance to a frightened ghost 
    # feature 7: shortest distance to intersection
    for i in range(5):
        for j in range(4):
            # features.append((BOARD.MAX_DIST - bfsRes[j][i]) / BOARD.MAX_DIST)
            t1, t2 = bfsRes[j][i]
            features.append(t1)
            features.append(t2)

    return features


# playable keyboard agent for pacman
class PlayableAgent(DirectionAgent):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        for val in pacmanFeatureExtraction(game):                
            print(val)

        print(np.array([[cell.val for cell in row] for row in game.state]))
        return super().getNextPos(game)

# deep q learning agent for pacman
class PacmanDQLAgent(DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return pacmanFeatureExtraction(game)
