from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.ghost import *
from data.config import POS
from data.data import GHOST_MODE, REP
from utils.coordinate import CPair
from utils.direction import DIR


# original agent for pinky
class PinkyClassicAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.PINKY, REP.PINKY, 0)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # scatter mode (head to corner)
        if self.mode == GHOST_MODE.SCATTER:
            return POS.PINKY_CORNER

        # chase mode
        targetTile: CPair = game.pacman.pos
        for _ in range(2):
            targetTile = targetTile.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(2):
                targetTile = targetTile.move(DIR.LF)

        return targetTile


# hyperaggressive agent for pinky
class PinkyClassicAggrAgent(ClassicGhostAgent):
    def __init__(self) -> None:
        super().__init__(POS.PINKY, REP.PINKY, 0)

    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        # chase mode
        targetTile: CPair = game.pacman.pos
        for _ in range(2):
            targetTile = targetTile.move(game.pacman.direction)

        # replicate target tile bug in classic pacman
        if game.pacman.direction == DIR.UP:
            for _ in range(2):
                targetTile = targetTile.move(DIR.LF)

        return targetTile


# static agent for pinky
class PinkyStaticAgent(StaticGhostAgent):
    def __init__(self) -> None:
        StaticGhostAgent.__init__(self, POS.PINKY, REP.PINKY)


# mdp solver for pinky
class PinkyMDPSolver(GhostMDPSolver):
    def __init__(self, game: "Game", rewards: dict[str, float]) -> None:
        GhostMDPSolver.__init__(self, game, rewards, REP.PINKY)


# mdp agent for pinky
class PinkyMDPAgent(MDPGhostAgent):
    def __init__(self, solver: type = PinkyMDPSolver, rewards: dict[str, float] = MDPGhostAgent.REWARDS) -> None:
        MDPGhostAgent.__init__(self, POS.PINKY, REP.PINKY, solver, rewards)

    # get regular movements (not dead)
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return MDPAgent.getNextPos(self, game)


# deep q learning agent for pinky
class PinkyDQLAgent(DQLGhostAgent):
    def __init__(self, neuralNet: NeuralNet) -> None:
        DQLGhostAgent.__init__(self, POS.PINKY, REP.PINKY, neuralNet)


# neuroevolution agent for pinky
class PinkyNEATAgent(NEATGhostAgent):
    def __init__(self, genome: Genome) -> None:
        NEATGhostAgent.__init__(self, POS.PINKY, REP.PINKY, genome)
