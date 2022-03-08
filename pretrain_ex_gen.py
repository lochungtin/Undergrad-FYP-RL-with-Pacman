import os
from time import sleep
from tkinter import Tk
import _thread
from typing import List

from agents.pacman import PacmanDQLAgent, PacmanMDPAgent, pacmanFeatureExtraction
from agents.blinky import BlinkyClassicAgent, BlinkyMDPAgent, blinkyFeatureExtraction
from agents.clyde import ClydeClassicAgent, ClydeClassicAggrAgent
from agents.inky import InkyClassicAgent, InkyClassicAggrAgent
from agents.pinky import PinkyClassicAgent, PinkyClassicAggrAgent
from data.data import REP
from game.game import Game
from gui.display import Display
from utils.file import loadNeuralNet
from utils.printer import printPacmanPerfomance


class MDPGuidedTraining:
    def __init__(self, config: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("MDP Guided Training")

            self.display: Display = Display(self.main)

        # reward constants
        self.rewards: dict[str, float] = config["rewards"]

        # mdp config
        self.mdpConfig: float = config["mdpConfig"]

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
        return Game(
            PacmanDQLAgent(loadNeuralNet("saves", "pacman", 70)),
            blinky=BlinkyMDPAgent(self.rewards, self.mdpConfig),
            # inky=InkyClassicAggrAgent(),
            # clyde=ClydeClassicAggrAgent(),
            pinky=PinkyClassicAggrAgent(),
        )

    # ===== main training function =====
    def training(self) -> None:
        epStart: int = 20
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
            features: List[float] = blinkyFeatureExtraction(game)
            features.append(game.ghosts[REP.BLINKY].direction)
            runFile = open("./out/BLINKY_MDP_EX/run{}.txt".format(epStart + eps), "a")
            runFile.write(str(features) + "\n")
            runFile.close()

            # rerender display if enabled
            if self.hasDisplay:
                self.display.rerender()

            # reset game when gameover
            if gameover or won or game.timesteps > 100:
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
    training: MDPGuidedTraining = MDPGuidedTraining(
        {
            "gameCap": 20,
            "mdpConfig": {
                "maxIter": 10000,
                "gamma": 0.90,
                "epsilon": 0.00005,
            },
            "rewards": {
                "ghost": 0,
                "pacmanF": -10,
                "pacmanR": 20,
                "timestep": -0.05,
            },
        },
        False,
    )
    training.start()
