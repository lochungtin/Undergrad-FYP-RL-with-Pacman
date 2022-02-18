from tkinter import Tk
from typing import List
import _thread
import numpy as np

from ai.deepq.neuralnet import NeuralNet
from agents.base import DirectionAgent
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
            DirectionAgent(POS.PACMAN, REP.PACMAN),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent()
        )

        self.main: Tk = Tk()
        self.main.title("NEAT Performance View")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        self.network = NeuralNet.load(filename)

        self.tc: TimeController = TimeController(0.05, self.nextStep)

        _thread.start_new_thread(self.tc.start, ())

    def processState(self, game: Game) -> List[int]:
        rt: List[int] = []

        for row in game.state:
            for cell in row:
                if REP.isGhost(cell):
                    rt.append(6)
                else:
                    rt.append(cell)

        return rt

    def nextStep(self):
        state: List[int] = self.processState(self.game)
        qVals: List[float] = self.network.predict(np.array([state]))
        self.game.pacman.setDir(np.argmax(qVals))

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
    epCount: int = 5000

    app = App("./{}/{}/rl_nnconf_ep{}.json".format(parent, runPref, epCount))
    app.run()
