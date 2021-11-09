from typing import Tuple

from ai.agents.agent import Agent
from ai.agents.pacman import PacmanAI
from ai.predictable import Predictable
from game.game import Game


class PAIV(Game):
    def __init__(
        self,
        predictable: Predictable,
        enableGhost: bool = True,
        enablePwrPlt: bool = True,
    ) -> None:
        super().__init__(enableGhost=enableGhost, enablePwrPlt=enablePwrPlt)

        self.pacman: Agent = PacmanAI(predictable)

        self.timesteps: int = 0
        self.pelletDrought: int = 0

    def nextStep(self) -> Tuple[bool, bool, bool]:
        self.timesteps += 1

        gameover, won, atePellet = super().nextStep()

        if atePellet:
            self.pelletDrought = 0
            
        self.pelletDrought += 1

        return gameover, won, atePellet