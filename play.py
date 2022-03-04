import _thread
from tkinter import Tk
from typing import List

import numpy as np


from agents.blinky import BlinkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from agents.pacman import PlayableAgent, pacmanFeatureExtraction
from data.config import BOARD
from data.data import GHOST_MODE
from utils.direction import DIR
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.grid import createGameSizeGrid


# app class
class App:
    def __init__(self, manualControl: bool) -> None:
        # create game object
        self.game: Game = self.newGame()

        # create time controller object
        self.timeController: TimeController = TimeController(0.1, self.nextStep)

        # create application
        self.main: Tk = Tk()
        self.main.title("Pacman")

        # bind key hanlders
        self.main.bind("<Up>", lambda _: self.game.pacman.setDir(DIR.UP))
        self.main.bind("<Down>", lambda _: self.game.pacman.setDir(DIR.DW))
        self.main.bind("<Left>", lambda _: self.game.pacman.setDir(DIR.LF))
        self.main.bind("<Right>", lambda _: self.game.pacman.setDir(DIR.RT))

        # create game display and bind game objects
        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        # bind nextStep() controllers
        if manualControl:
            self.main.bind("<space>", lambda _: self.nextStep())
        else:
            _thread.start_new_thread(self.timeController.start, ())

    def newGame(self):
        return Game(
            PlayableAgent(),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent(),
        )

    # trigger Game.nextStep() and update dislay, reset if gameover
    def nextStep(self):
        # update game, proceed to next step
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()

        for row in self.makeRewardGrid(self.game):
            print(row)
        print()

        # handle gameover
        if gameover or won:
            print(self.game.timesteps)

            # create new game
            self.game = self.newGame()
            self.display.newGame(self.game)

        # update display
        self.display.rerender()

    # run main loop of application
    def run(self) -> None:
        self.main.mainloop()


    def makeRewardGrid(self, game: Game) -> List[List[float]]:
        rewardGrid: List[List[float]] = createGameSizeGrid(-1)

        for ghost in game.ghostList:
            if not ghost.isDead:
                if ghost.isFrightened:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = (
                        20 * game.pwrpltEffectCounter / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT
                    )
                else:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = -100

        for key, pwrplt in game.pwrplts.items():
            if pwrplt.valid:
                avgGhostDist: float = 1
                for ghost in game.ghostList:
                    if not ghost.isDead:
                        avgGhostDist += pwrplt.pos.manDist(ghost.pos)

                avgGhostDist /= len(game.ghostList)

                rewardGrid[pwrplt.pos.row][pwrplt.pos.col] = 50 * (1 / avgGhostDist ** 2)

        for key, pellet in game.pellets.items():
            if pellet.valid:
                rewardGrid[pellet.pos.row][pellet.pos.col] = 5 * ((BOARD.TOTAL_PELLET_COUNT - game.pelletProgress + 1) / BOARD.TOTAL_PELLET_COUNT)

        return rewardGrid


# execute app
if __name__ == "__main__":
    App(manualControl=True).run()
