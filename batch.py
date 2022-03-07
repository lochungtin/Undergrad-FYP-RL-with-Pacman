import os
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
from data.config import BOARD
from gui.controller import TimeController
from gui.display import Display
from utils.printer import printPacmanPerfomance


# load neural network from config json
def loadNeuralNet(parentFolder: str, prefix: str, ep: int) -> NeuralNet:
    return NeuralNet.load("./{}/{}/rl_nnconf_ep{}.json".format(parentFolder, prefix, ep))


# load genome from config json
def loadGenome(parentFolder: str, prefix: str, gen: int) -> Genome:
    return GenomeUtils.load("./{}/{}/ga_nnconf_ep{}.json".format(parentFolder, prefix, gen))


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

    def nextStep(self):
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()

        if ateGhost:
            self.kills += 1

        if not self.game.pacman.moved:
            self.stationary += 1

        if gameover or won:
            return False, printPacmanPerfomance(0, self.game, False)

        if self.game.timesteps > 1000:
            # print()
            return False, 0

        return True, 0

    def run(self) -> None:
        running: bool = True
        completion: float = 0
        while running:
            running, completion = self.nextStep()

        return completion


if __name__ == "__main__":
    # save: dict[str, int] = {}
    path: str = "./out/RL0703_2040"
    
    # files: List[str] = os.listdir(path)
    files: dict[str, int] = {
        "rl_nnconf_ep1578.json": 0,
        "rl_nnconf_ep1831.json": 0,
        "rl_nnconf_ep1605.json": 0,
        "rl_nnconf_ep1829.json": 0,
        "rl_nnconf_ep2310.json": 0,
        "rl_nnconf_ep2191.json": 0,
    }

    for i in range(50):
        print("iteration: {}".format(i))
        for file, count in files.items():
            appConfig: dict[str, object] = {
                "agents": {
                    "pacman": PacmanDQLAgent(NeuralNet.load("{}/{}".format(path, file))),
                    "blinky": BlinkyClassicAgent(),
                    "inky": None,
                    "clyde": None,
                    "pinky": PinkyClassicAgent(),
                },
                "display": False,
                "enablePwrPlt": True,
                "gameSpeed": 0.05,
            }

            files[file] += App(appConfig).run()

    for file, count in files.items():
        print(file, count / 50)