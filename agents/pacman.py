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

    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return super().getNextPos(game)


# deep q learning agent for pacman
class PacmanDQLAgent(DQLAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN, neuralNet)

    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        return pacmanFeatureExtraction(game)
