from tkinter import Tk
from typing import List
import _thread
import numpy as np

from ai.deepq.neuralnet import NeuralNet
from ai.deepq.utils import NNUtils
from agents.base import DirectionAgent, DGhostAgent
from agents.blinky import BlinkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from data.data import BOARD, POS, REP
from data.config import CONFIG
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.coordinate import CPair


class App:
    def __init__(self, filename) -> None:
        self.game = Game(
            DirectionAgent(POS.PACMAN, REP.PACMAN),
            BlinkyClassicAgent(),
            DGhostAgent(POS.INKY, REP.INKY),
            DGhostAgent(POS.CLYDE, REP.CLYDE),
            DGhostAgent(POS.PINKY, REP.PINKY),
            enableGhost=True,
            enablePwrPlt=False,
        )

        self.main: Tk = Tk()
        self.main.title("NEAT Performance View")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        self.network = NeuralNet.load(filename)

        self.timeController: TimeController = TimeController(0.05, self.nextStep)

        _thread.start_new_thread(self.timeController.start, ())

    def processState(self, game: Game) -> List[int]:
        rt: List[int] = []

        for i, row in enumerate(CONFIG.BOARD):
            for j, cell in enumerate(row):
                if cell == REP.EMPTY:
                    rt.append(game.state[i][j])

        return rt

    def nextStep(self):
        state: List[int] = self.processState(self.game)
        qVals: List[float] = self.network.predict(np.array([state]))
        self.game.pacman.setDir(np.argmax(qVals))

        gameover, won, atePellet, pacmanMoved = self.game.nextStep()

        if gameover or won:
            self.timeController.end()
            self.main.destroy()

        self.display.rerender(atePellet)

    def run(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":
    parent: str = "out"
    runPref: str = "RL1702_2022"
    epCount: int = 2000

    app = App("./{}/{}/rl_nnconf_ep{}.json".format(parent, runPref, epCount))
    app.run()
