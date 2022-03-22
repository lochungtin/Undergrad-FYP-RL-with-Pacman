from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.base import DirectionAgent
from utils.coordinate import CPair


class MDPAgent(DirectionAgent):
    def __init__(self, pos: CPair, repId: int, solver: type, rewards: dict[str, float]) -> None:
        super().__init__(pos, repId)

        # mdp solver
        self.solver: type = solver

        # rewards
        self.rewards: dict[str, float] = rewards

    # get next position
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.setDir(self.solver(game, self.rewards).getAction(self.pos))
        return super().getNextPos(game)
