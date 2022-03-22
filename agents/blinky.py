from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.base import DirectionAgent, GhostAgent
from agents.base.ghost import ClassicGhostAgent, DQLGhostAgent, GhostMDPSolver, MDPGhostAgent
from agents.base.mdp import MDPAgent
from ai.deepq.neuralnet import NeuralNet
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair


# original agent for blinky
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


# hyperaggressive agent for blinky
class BlinkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        ClassicGhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, 0)

        self.cruiseElroy: bool = False

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # chase mode
        return game.pacman.pos


# mdp solver for blinky
class BlinkyMDPSolver(GhostMDPSolver):
    def __init__(self, game: "Game", rewards: dict[str, float]) -> None:
        GhostMDPSolver.__init__(self, game, rewards, REP.BLINKY)


# mdp agent for blinky
class BlinkyMDPAgent(MDPGhostAgent):
    def __init__(self, solver: type = BlinkyMDPSolver, rewards: dict[str, float] = MDPGhostAgent.REWARDS) -> None:
        MDPGhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, solver, rewards)

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return MDPAgent.getNextPos(self, game)


# deep q learning training agent for blinky
class BlinkyDQLTAgent(GhostAgent, DirectionAgent):
    def __init__(self) -> None:
        GhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, False)
        DirectionAgent.__init__(self, POS.BLINKY, REP.BLINKY)

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return DirectionAgent.getNextPos(self, game)


# deep q learning agent for blinky
class BlinkyDQLAgent(DQLGhostAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        DQLGhostAgent.__init__(self, POS.BLINKY, REP.BLINKY, neuralNet)
