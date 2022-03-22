from tkinter import Tk
import _thread

import numpy as np
from agents.base import StaticGhostAgent

from agents.blinky import BlinkyClassicAgent, BlinkyDQLAgent, blinkyFeatureExtraction
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from agents.pacman import PacmanDQLAgent
from data.data import AGENT_CLASS_TYPE, REP
from data.config import POS
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.file import loadNeuralNet
from utils.game import newGame, newRndORGLGhostGame
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # create game
        self.game: Game = newGame(
            config["ghosts"],
            config["enablePwrPlt"],
            config["neuralnets"],
            config["genomes"],
        )

        # creat gui
        self.main: Tk = Tk()
        self.main.title("Auto Pacman Game Viewer")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        # create and enable auto timestep controller
        self.tc: TimeController = TimeController(config["gameSpeed"], self.nextStep)

        _thread.start_new_thread(self.tc.start, ())

    # perform update step
    def nextStep(self):
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()
        self.display.rerender()

        if gameover or won:
            printPacmanPerfomance(0, self.game)

            self.tc.end()
            self.main.destroy()

    # run gui
    def start(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":

    app: App = App(
        {
            "enablePwrPlt": True,
            "gameSpeed": 0.10,
            "genomes": {},
            "ghosts": {
                REP.BLINKY: AGENT_CLASS_TYPE.GDQL,
                REP.INKY: AGENT_CLASS_TYPE.NONE,
                REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                REP.PINKY: AGENT_CLASS_TYPE.OGNL,
            },
            "neuralnets": {
                "pacman": ("saves", "pacman", 63),
                REP.BLINKY: ("out", "RL2103_1506", 9000),
            },
        }
    )
    app.start()
