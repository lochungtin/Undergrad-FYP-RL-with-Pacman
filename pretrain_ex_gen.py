from random import choice
from tkinter import Tk
from typing import List
import _thread
import numpy as np
import os


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
        ghost: int = np.random.randint(0, 3)
        gType: int = np.random.randint(0, 2)
        pType: int = np.random.randint(0, 2)

        inky, clyde, pinky = None, None, None

        if ghost == 0:
            if gType == 0:
                inky = InkyClassicAgent()
            else:
                inky = InkyClassicAggrAgent()
        elif ghost == 1:
            if gType == 0:
                clyde = ClydeClassicAgent()
            else:
                clyde = ClydeClassicAggrAgent()
        else:
            if gType == 0:
                pinky = PinkyClassicAgent()
            else:
                pinky = PinkyClassicAggrAgent()

        if True and pType == 0:
            pacman = PacmanDQLAgent(loadNeuralNet("saves", "pacman", choice([50, 52, 55, 60, 63])))
        else:
            pacman = PacmanMDPAgent()

        return Game(
            pacman=pacman,
            blinky=BlinkyMDPAgent(),
            inky=inky,
            clyde=clyde,
            pinky=pinky,
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
            features: List[float] = blinkyFeatureExtraction(game)
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
