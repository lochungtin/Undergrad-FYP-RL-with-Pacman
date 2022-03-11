from tkinter import Tk
import _thread

import numpy as np
from agents.base import StaticGhostAgent

from agents.blinky import BlinkyClassicAgent, BlinkyDQLAgent, blinkyFeatureExtraction
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from agents.pacman import PacmanDQLAgent
from data.data import GHOST_CLASS_TYPE, REP
from data.config import POS
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.file import loadNeuralNet
from utils.game import newRndORGLGhostGame
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # create game
        self.game: Game = newRndORGLGhostGame(config["enablePwrPlt"], config["neuralnets"])

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
            "neuralnets": {"pacman": ("saves", "pacman", 63)},
        }
    )
    app.start()
