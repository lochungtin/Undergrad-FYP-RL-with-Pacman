from tkinter import Tk
from typing import List
import _thread
import numpy as np

from ai.deepq.neuralnet import NeuralNet
from ai.deepq.utils import NNUtils
from agents.base import DirectionAgent
from agents.blinky import BlinkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from data.data import BOARD, POS, REP
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.coordinate import CPair


class App:
    def __init__(self, filename) -> None:
        self.game = Game(
            DirectionAgent(POS.PACMAN, REP.PACMAN),
            BlinkyClassicAgent(),
            InkyClassicAgent(),
            ClydeClassicAgent(),
            PinkyClassicAgent(),
            enableGhost=False,
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

        pacPos: CPair = game.pacman.pos
        pRow, pCol, = (
            pacPos.row,
            pacPos.col,
        )

        # valid actions
        for pos in pacPos.getNeighbours(True):
            if hasattr(pos, "row"):
                rt.append(int(not REP.isWall(game.state[pos.row][pos.col])))
            else:
                rt.append(0)

        # pacman data
        rt.append(pRow)
        rt.append(pCol)

        # ghost data
        # for ghost in game.ghosts:
        #     gRow, gCol = ghost.pos.row, ghost.pos.col
        #     rt.append(gRow)
        #     rt.append(gCol)
        #     rt.append(int(ghost.isDead))
        #     rt.append(int(ghost.isFrightened))
        for i in range(16):
            rt.append(0)

        # pellet data
        minDist: int = BOARD.row + BOARD.col + 2
        minR: int = -1
        minC: int = -1

        for r in range(BOARD.row):
            for c in range(BOARD.col):
                cell: int = game.state[r][c]
                if cell == REP.PELLET:
                    dist: int = abs(pRow - r) + abs(pCol - c)
                    if dist < minDist:
                        minDist = dist
                        minR = r
                        minC = c

        rt.append(minR)
        rt.append(minC)
        rt.append(game.pelletCount)

        return rt

    def nextStep(self):
        state: List[int] = self.processState(self.game)
        qVals: List[float] = self.network.predict(np.array([state]))
        self.game.pacman.setDir(np.argmax(qVals))

        gameover, won, atePellet = self.game.nextStep()

        if gameover or won:
            self.timeController.end()
            self.main.destroy()

        self.display.rerender(atePellet)

    def run(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":
    parent: str = "out"
    runPref: str = "RL1702_0403"
    epCount: int = 300

    app = App("./{}/{}/rl_nnconf_ep{}.json".format(parent, runPref, epCount))
    app.run()
