from queue import Queue
from typing import List, Tuple, TYPE_CHECKING

from ai.deepq.neuralnet import NeuralNet

if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent, DQLAgent, DirectionAgent, GhostAgent, distanceComparison
from ai.mdp.solver import Solver
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.grid import createGameSizeGrid


def blinkyFeatureExtraction(game: "Game") -> List[float]:
    features: List[float] = [0, 0, 0, 0]

    # blinky data
    blinky: GhostAgent = game.ghosts[REP.BLINKY]
    bPos: CPair = blinky.pos
    bCell: Cell = game.getCell(bPos)

    # pacman data
    pPos: CPair = game.pacman.pos
    pCell: Cell = game.getCell(pPos)

    # feature 1: valid directions
    for action, neighbour in bCell.adj.items():
        if not neighbour is None:
            features[action] = 1

    # feature 2: frightened state
    features.append((game.pwrpltEffectCounter + 1) * blinky.isFrightened / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT)

    # feature 3: nearest intersection to blinky
    # openlist: Queue[Cell] = Queue()
    # openlist.put(pCell)
    # closedList: List[List[bool]] = createGameSizeGrid(False)

    # curCell: Cell = None
    # while not openlist.empty():
    #     # get current visiting cell
    #     curCell = openlist.get()

    #     # update closed list
    #     closedList[curCell.coords.row][curCell.coords.col] = True

    #     # break condition
    #     if curCell.isIntersection():
    #         break

    #     # add unvisited neighbours to openlist
    #     for neighbour in curCell.getValidNeighbours():
    #         if not closedList[neighbour.coords.row][neighbour.coords.col]:
    #             openlist.put(neighbour)

    # features += distanceComparison(bPos, curCell.coords)

    # feature 4: pacman position
    features += distanceComparison(bPos, pPos)

    # feature 5: nearest intersections to pacman
    # openlist = Queue()
    # openlist.put(pCell)
    # closedList = createGameSizeGrid(False)

    # intersections: List[CPair] = []
    # if pCell.isIntersection():
    #     intersections = [bPos, bPos]
    # else:
    #     while not openlist.empty():
    #         # get current visiting cell
    #         curCell: Cell = openlist.get()

    #         # update closed list
    #         closedList[curCell.coords.row][curCell.coords.col] = True

    #         # add intersection to list
    #         if curCell.isIntersection():
    #             intersections.append(curCell.coords)

    #         # break condition
    #         if len(intersections) == 2:
    #             break

    #         # add unvisited neighbours to openlist
    #         for neighbour in curCell.getValidNeighbours():
    #             if not closedList[neighbour.coords.row][neighbour.coords.col]:
    #                 openlist.put(neighbour)

    # # add intersection to feature vector
    # for intersection in intersections:
    #     features += distanceComparison(bPos, intersection)
    #     features.append(bPos.manDist(intersection) / BOARD.MAX_DIST)

    return features


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
    def __init__(self, game: "Game", rewards: dict[str, float], config: dict[str, object]) -> None:
        super().__init__(game, rewards, config)

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
    def __init__(self, rewards: dict[str, float], mdpConfig: dict[str, float]) -> None:
        GhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, False)
        DirectionAgent.__init__(self, POS.BLINKY, REP.BLINKY)

        # reward values
        self.rewards: dict[str, float] = rewards

        # mdp config
        self.mdpConfig: dict[str, float] = mdpConfig

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.setDir(BlinkyMDPSolver(game, self.rewards, self.mdpConfig).getAction(self.pos))
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
        return blinkyFeatureExtraction(game)

    # get regular movement (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return DQLAgent.getNextPos(self, game)
