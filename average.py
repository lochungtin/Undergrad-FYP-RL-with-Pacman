from copy import deepcopy
from tkinter import Tk
import _thread

from agents.base import Agent, GhostAgent
from agents.blinky import BlinkyClassicAgent, BlinkyClassicAggrAgent
from agents.inky import InkyClassicAgent, InkyClassicAggrAgent
from agents.clyde import ClydeClassicAgent, ClydeClassicAggrAgent
from agents.pacman import PacmanDQLAgent
from agents.pinky import PinkyClassicAgent, PinkyClassicAggrAgent
from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils
from game.game import Game
from utils.file import loadNeuralNet
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, appConfig: dict[str, object]) -> None:
        # game config
        self.ghosts: dict[str, GhostAgent] = appConfig["ghosts"]
        self.pwrplt: bool = appConfig["enablePwrPlt"]

        # iterations
        self.iterations: int = appConfig["iterations"]

        # neural net
        self.neuralnets: NeuralNet = appConfig["neuralnets"]

    def start(self) -> None:
        average: float = 0

        for i in range(self.iterations):
            average += self.runGame()

        print("Average Completion Rate: {}".format(average / self.iterations))

    def runGame(self) -> float:
        game: Game = self.newGame(self.neuralnets["pacman"])

        kills: int = 0
        stationary: int = 0

        while True:
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            if ateGhost:
                kills += 1

            if not game.pacman.moved:
                stationary += 1

            if gameover or won:
                return printPacmanPerfomance(0, game, True)

            if game.timesteps > 1000:
                break

        return 0

    def newGame(self, pacmanNet: NeuralNet) -> Game:
        blinky: GhostAgent = None
        if self.ghosts["blinky"]:
            blinky = BlinkyClassicAgent()

        inky: GhostAgent = None
        if self.ghosts["inky"]:
            inky = InkyClassicAgent()

        clyde: GhostAgent = None
        if self.ghosts["clyde"]:
            clyde = ClydeClassicAgent()

        pinky: GhostAgent = None
        if self.ghosts["pinky"]:
            pinky = PinkyClassicAgent()

        return Game(PacmanDQLAgent(pacmanNet), blinky, inky, clyde, pinky, self.pwrplt)


if __name__ == "__main__":
    app: App = App({
        "ghosts": {
            "blinky": True,
            "inky": False,
            "clyde": False,
            "pinky": True,
        },
        "enablePwrPlt": True,
        "iterations": 100,
        "neuralnets": {
            "pacman": loadNeuralNet("out", "RL0703_2107", 5895)
        }
    })
    app.start()
