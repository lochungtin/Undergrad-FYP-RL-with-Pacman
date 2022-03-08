from typing import List, Tuple, TYPE_CHECKING

from ai.mdp.solver import Solver
from game.utils.cell import Cell
from utils.grid import createGameSizeGrid


if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent, DirectionAgent, GhostAgent, distanceComparison
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair


def blinkyFeatureExtraction(game: "Game") -> List[float]:
    features: List[float] = [0, 0, 0, 0]

    blinky: GhostAgent = game.ghosts[REP.BLINKY]
    bPos: CPair = blinky.pos
    bCell: Cell = game.getCell(bPos)

    # feature 1: valid directions
    for action, neighbour in bCell.adj.items():
        if not neighbour is None:
            features[action] = 1

    # feature 2: distance to pacman
    features += distanceComparison(bPos, game.pacman.pos)
    features.append((game.pwrpltEffectCounter + 1) * blinky.isFrightened / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT)

    # feature 3: distance to neighbouring ghost
    g: GhostAgent = None
    for ghost in game.ghostList:
        if ghost.repId != REP.BLINKY:
            g = ghost

    features += distanceComparison(bPos, g.pos)
    features.append((game.pwrpltEffectCounter + 1) * g.isFrightened / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT)

    return features

# classic ai agent for blinky
class BlinkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0)

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
        super().__init__(POS.BLINKY, REP.BLINKY, 0)

        self.cruiseElroy: bool = False

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # chase mode
        return game.pacman.pos


# mdp agent for blinky
class BlinkyMDPSolver(Solver):
    def __init__(self, game: "Game", rewards: dict[str, float], config: dict[str, object]) -> None:
        super().__init__(game, rewards, config)

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

    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.setDir(BlinkyMDPSolver(game, self.rewards, self.mdpConfig).getAction(self.pos))
        return DirectionAgent.getNextPos(self, game)


# deep q learning training agent for blinky
class BlinkyDQLTAgent(GhostAgent, DirectionAgent):
    def __init__(self) -> None:
        GhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, False)
        DirectionAgent.__init__(self, POS.BLINKY, REP.BLINKY)

    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return DirectionAgent.getNextPos(self, game)