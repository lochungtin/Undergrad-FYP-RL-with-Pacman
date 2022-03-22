from random import choice
from tkinter import Tk
from typing import List, Tuple
import _thread
import numpy as np
import os

from agents.utils.features import ghostFeatureExtraction, pacmanFeatureExtraction
from data.data import AGENT_CLASS_TYPE, REP
from game.game import Game, newGame
from gui.display import Display
from utils.printer import printPacmanPerfomance


class MDPGuidedTraining:
    def __init__(self, config: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("MDP Guided Training")

            self.display: Display = Display(self.main)

        # training config
        self.gameCap: int = config["gameCap"]

    # start training (main function)
    def start(self) -> None:
        # start display
        if self.hasDisplay:
            _thread.start_new_thread(self.training, ())
            self.main.mainloop()

        else:
            self.training()

    def newGame(self) -> Game:
        pacmanType: int = AGENT_CLASS_TYPE.SMDP
        pacmanNN: Tuple[str, str, int] = None
        if np.random.rand() > 0.5:
            pacmanType = AGENT_CLASS_TYPE.GDQL
            pacmanNN = ("saves", "pacman", choice([50, 52, 55, 60, 63]))

        return newGame(
            {
                REP.PACMAN: pacmanType,
                REP.BLINKY: AGENT_CLASS_TYPE.SMDP,
                "secondary": AGENT_CLASS_TYPE.RAND,
            },
            True,
            {
                REP.PACMAN: pacmanNN,
            },
            {},
        )

    # ===== main training function =====
    def training(self) -> None:
        epStart: int = 0
        eps: int = 0

        # create new game
        game: Game = self.newGame()
        if self.hasDisplay:
            self.display.newGame(game)

        # create new save file for new run
        open("./out/BLINKY_MDP_EX/run{}.txt".format(epStart + eps), "x")

        while True:
            # perform next step
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            # save array
            features: List[float] = ghostFeatureExtraction(game, REP.BLINKY)
            features.append(game.ghosts[REP.BLINKY].direction)

            runFile = open("./out/BLINKY_MDP_EX/run{}.txt".format(epStart + eps), "a")
            runFile.write(str(features) + "\n")
            runFile.close()

            # rerender display if enabled
            if self.hasDisplay:
                self.display.rerender()

            # reset game when gameover
            if gameover or won or game.timesteps > 200:
                printPacmanPerfomance(eps, game)

                # exit loop
                eps += 1
                if eps >= self.gameCap:
                    break

                # create new game
                game = self.newGame()
                if self.hasDisplay:
                    self.display.newGame(game)

                # create new save file for new run
                open("./out/BLINKY_MDP_EX/run{}.txt".format(epStart + eps), "x")


if __name__ == "__main__":
    training: MDPGuidedTraining = MDPGuidedTraining({"gameCap": 1000}, True)
    training.start()
