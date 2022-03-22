from queue import Queue
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.agent import GhostAgent
from data.config import BOARD
from data.data import GHOST_MODE
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.grid import createGameSizeGrid

# pacman feature extraction function
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

        # break condition
        if curCell.hasPellet:
            closestPellet = curCell.coords
            break

        # add unvisited neighbours to openlist
        for neighbour in curCell.getValidNeighbours():
            if not closedList[neighbour.coords.row][neighbour.coords.col]:
                openlist.put(neighbour)

    features += BOARD.relativeDistance(pPos, closestPellet)

    # feature 3: relative position to closest power pellet
    closestPwrplt: CPair = pPos
    closestPwrpltD: int = BOARD.MAX_DIST
    for key, pwrplt in game.pwrplts.items():
        if pwrplt.valid:
            d: int = pPos.manDist(pwrplt.pos)
            if d < closestPwrpltD:
                closestPwrplt = pwrplt.pos
                closestPwrpltD = d

    features += BOARD.relativeDistance(pPos, closestPwrplt)

    # feature 4: relative position to #1 closest ghost + ghost state
    g0: GhostAgent = game.ghostList[0]
    if g0.isDead:
        features += [0, 0, 0, 0, 0]
    else:
        features += BOARD.relativeDistance(pPos, g0.pos)
        features.append(g0.isFrightened * 1)

    # feature 5: relative position to #2 closest ghost + ghost state
    g1: GhostAgent = game.ghostList[1]
    if g1.isDead:
        features += [0, 0, 0, 0, 0]
    else:
        features += BOARD.relativeDistance(pPos, g1.pos)
        features.append(g1.isFrightened * 1)

    return features


# ghost feature extraction function
def ghostFeatureExtraction(game: "Game", repId: int) -> List[float]:
    features: List[float] = [0, 0, 0, 0]

    # ghost data
    ghost: GhostAgent = game.ghosts[repId]
    bPos: CPair = ghost.pos
    bCell: Cell = game.getCell(bPos)

    # pacman data
    pPos: CPair = game.pacman.pos
    pCell: Cell = game.getCell(pPos)

    # feature 1: valid directions
    for action, neighbour in bCell.adj.items():
        if not neighbour is None:
            features[action] = 1

    # feature 2: frightened state
    features.append((game.pwrpltEffectCounter + 1) * ghost.isFrightened / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT)

    # feature 3: pacman position
    features += BOARD.relativeDistance(bPos, pPos)

    return features
