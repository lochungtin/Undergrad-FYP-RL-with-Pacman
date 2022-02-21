from tkinter import Tk
from typing import List
import _thread
import numpy as np

from agents.pacman import PacmanDQLAgent
from agents.blinky import BlinkyClassicAgent
from agents.inky import InkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.pinky import PinkyClassicAgent
from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils
from game.game import Game
from gui.controller import TimeController
from gui.display import Display


class App:
    def __init__(self, gameConfig: dict[str, object]) -> None:
        self.game = Game(
            gameConfig["agents"]["pacman"],
            blinky=gameConfig["agents"]["blinky"],
            inky=gameConfig["agents"]["inky"],
            clyde=gameConfig["agents"]["clyde"],
            pinky=gameConfig["agents"]["pinky"],
            enablePwrPlt=gameConfig["enablePwrPlt"],
        )

        self.pellets: int = 0
        self.kills: int = 0
        self.stationary: int = 0

        self.main: Tk = Tk()
        self.main.title("Auto Pacman Game Viewer")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        self.tc: TimeController = TimeController(
            gameConfig["gameSpeed"], self.nextStep)

        _thread.start_new_thread(self.tc.start, ())

    def nextStep(self):
        gameover, won, atePellet, ateGhost, pacmanMoved = self.game.nextStep()

        if atePellet:
            self.pellets += 1

        if ateGhost: 
            self.kills += 1

        if not pacmanMoved:
            self.stationary += 1

        if gameover or won:
            print("P: {}/{} K: {} S: {}/{}".format(
                self.pellets,
                self.pellets + self.game.pelletProgress,
                self.kills,
                self.stationary,
                self.game.timesteps,
            ))

            self.tc.end()
            self.main.destroy()

        self.display.rerender(atePellet)

    def run(self) -> None:
        self.main.mainloop()


# load neural network from config json
def loadNeuralNet(parentFolder: str, prefix: str, ep: int) -> NeuralNet:
    return NeuralNet.load("./{}/{}/rl_nnconf_ep{}.json".format(parentFolder, prefix, ep))


# load genome from config json
def loadGenome(parentFolder: str, prefix: str, gen: int) -> Genome:
    return GenomeUtils.load("./{}/{}/ga_nnconf_ep{}.json".format(parentFolder, prefix, gen))


if __name__ == "__main__":
    gameConfig: dict[str, object] = {
        "agents": {
            "pacman": PacmanDQLAgent(loadNeuralNet("out", "RL2002_1435", 10500)),
            "blinky": BlinkyClassicAgent(),
            "inky": None,
            "clyde": None,
            "pinky": PinkyClassicAgent(),
        },
        "enablePwrPlt": True,
        "gameSpeed": 0.10,
    }

    App(gameConfig).run()
