from queue import Queue
from typing import List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from game.game import Game

from ai.deepq.neuralnet import NeuralNet
from agents.base import DQLAgent, DirectionAgent, GhostAgent
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from game.utils.cell import Cell
from utils.coordinate import CPair


def bfs(starting: Cell, origin: Cell, game: "Game") -> List[int]:
    # targets: [pellet, power pellet, ghost, scared ghost, intersection]
    distances: List[int] = [0, 0, 0, 0, 0]
    completed: List[int] = [False, False, False, False, False]

    openList: Queue[Tuple[int, Cell]] = Queue()
    openList.put((0, starting))

    closedList: List[List[bool]] = [[False for j in range(BOARD.COL)] for i in range(BOARD.ROW)]
    closedList[origin.coords.row][origin.coords.col] = True

    # premetively check power pellets and ghosts states to minimise computation
    # check if all power pellets are used
    allUsed: bool = True
    for id, pwrplts in game.pwrplts.items():
        allUsed = allUsed and not pwrplts.valid

    if allUsed:
        completed[1] = True
        distances[1] = BOARD.MAX_DIST

    # check if any ghosts are dead or frightened
    noHostiles: bool = True
    noFrightened: bool = True
    for ghost in game.ghostList:
        noHostiles *= ghost.isDead or ghost.isFrightened
        noFrightened *= not ghost.isFrightened

    if noHostiles:
        completed[2] = True
        distances[2] = BOARD.MAX_DIST

    if noFrightened:
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
            completed[4] = True

        # check values
        if curCell.occupied():
            if not completed[0] and curCell.hasPellet:
                completed[0] = True

            elif not completed[1] and curCell.hasPwrplt:
                completed[1] = True

            elif curCell.hasGhost:
                for id, presence in curCell.ghosts.items():
                    if presence:
                        if not completed[2] and not game.ghosts[id].isDead:
                            completed[2] = True

                        elif not completed[3] and game.ghosts[id].isFrightened:
                            completed[3] = True

        # check if all targets are found
        allDone: bool = True
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

    return distances


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
    for data in range(4):
        for dir in range(4):
            val: float = bfsRes[dir][data]

            if data == 2:
                val = max(val - bfsRes[dir][4], 0)

            # normalise and append value
            features.append(BOARD.MAX_DIST - val / BOARD.MAX_DIST)

    return features


# playable keyboard agent for pacman
class PlayableAgent(DirectionAgent):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)

    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return super().getNextPos(game)


# deep q learning agent for pacman
class PacmanDQLAgent(DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return pacmanFeatureExtraction(game)
