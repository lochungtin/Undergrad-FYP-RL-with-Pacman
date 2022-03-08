from typing import List, Tuple, TYPE_CHECKING

from ai.mdp.solver import Solver
from utils.grid import createGameSizeGrid


if TYPE_CHECKING:
    from game.game import Game

from agents.base import ClassicGhostAgent, DirectionAgent, GhostAgent
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair


# classic ai agent for blinky
class BlinkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, 0)

        self.cruiseElroy: bool = False

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

        # scatter mode (head to corner)
        elif self.mode == GHOST_MODE.SCATTER:
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
        # dead
        if self.isDead:
            return POS.GHOST_HOUSE_CENTER

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


class BlinkyMDPAgent(DirectionAgent):
    def __init__(self, rewards: dict[str, float], mdpConfig: dict[str, float]) -> None:
        super().__init__( POS.BLINKY, REP.BLINKY)

        self.isDead: bool = False
        self.isFrightened: bool = False
        self.speedReducer: int = 0

        self.isClassic: bool = False

        # reward values
        self.rewards: dict[str, float] = rewards

        # mdp config
        self.mdpConfig: dict[str, float] = mdpConfig

    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.setDir(BlinkyMDPSolver(game, self.rewards, self.mdpConfig).getAction(self.pos))
        return super().getNextPos(game)
