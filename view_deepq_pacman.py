from tkinter import Tk
from typing import List
import _thread
import numpy as np

from ai.deepq.neuralnet import NeuralNet
from agents.pacman import PacmanDQLAgent
from agents.blinky import BlinkyClassicAgent
from agents.inky import InkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.pinky import PinkyClassicAgent
from data.data import POS, REP
from game.game import Game
from gui.controller import TimeController
from gui.display import Display


class App:
    def __init__(self, filename) -> None:
        self.game = Game(
            PacmanDQLAgent(NeuralNet.load(filename)),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent()
        )

        self.main: Tk = Tk()
        self.main.title("NEAT Performance View")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        self.tc: TimeController = TimeController(0.10, self.nextStep)

        _thread.start_new_thread(self.tc.start, ())

    def nextStep(self):
        gameover, won, atePellet, ateGhost, pacmanMoved = self.game.nextStep()

        if gameover or won:
            self.tc.end()
            self.main.destroy()

        self.display.rerender(atePellet)

    def run(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":
    parent: str = "out"
    runPref: str = "RL1802_1614"
    epCount: int = 12000

    app = App("./{}/{}/rl_nnconf_ep{}.json".format(parent, runPref, epCount))
    app.run()
