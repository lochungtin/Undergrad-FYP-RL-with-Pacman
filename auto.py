from tkinter import Tk
import _thread

from agents.pacman import PacmanDQLAgent
from agents.blinky import BlinkyClassicAgent, BlinkyClassicAggrAgent
from agents.inky import InkyClassicAgent, InkyClassicAggrAgent
from agents.clyde import ClydeClassicAgent, ClydeClassicAggrAgent
from agents.pinky import PinkyClassicAgent, PinkyClassicAggrAgent
from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.file import loadNeuralNet
from utils.printer import printPacmanPerfomance


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

        self.tc: TimeController = TimeController(gameConfig["gameSpeed"], self.nextStep)

        _thread.start_new_thread(self.tc.start, ())

    def nextStep(self):
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()

        if ateGhost:
            self.kills += 1

        if not self.game.pacman.moved:
            self.stationary += 1

        if gameover or won:
            printPacmanPerfomance(0, self.game)

            self.tc.end()
            self.main.destroy()

        self.display.rerender()

    def run(self) -> None:
        self.main.mainloop()

if __name__ == "__main__":
    app: App = App({
        "agents": {
            "pacman": PacmanDQLAgent(loadNeuralNet("out", "RL0703_2107", 5905)),
            "blinky": BlinkyClassicAgent(),
            "inky": None,
            "clyde": None,
            "pinky": PinkyClassicAgent(),
        },
        "enablePwrPlt": True,
        "gameSpeed": 0.05,
    })
    app.run()
