from copy import deepcopy
from ctypes import util
from datetime import datetime
from tkinter import Tk
from typing import List, Tuple
import _thread
import numpy as np
import os
import time

from agents.base import DirectionAgent
from agents.pacman import pacmanFeatureExtraction
from ai.deepq.adam import Adam
from ai.deepq.neuralnet import NeuralNet
from ai.deepq.replaybuf import ReplayBuffer
from ai.deepq.utils import NNUtils
from agents.blinky import BlinkyClassicAgent
from agents.pinky import PinkyClassicAgent
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from game.game import Game
from gui.display import Display
from utils.coordinate import CPair
from utils.grid import createGameSizeGrid


class MDPGuidedTraining:
    def __init__(self, trainingConfig: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("MDP Guided Training")

            self.display: Display = Display(self.main)

        # mdp config
        self.gamma: int = trainingConfig["mdpConfig"]["gamma"]
        self.epsilon: int = trainingConfig["mdpConfig"]["epsilon"]

        self.maxIter: int = trainingConfig["mdpConfig"]["maxIterations"]

        # reward constants
        self.rewards: dict[str, float] = trainingConfig["rewards"]

    # start training (main function)
    def start(self) -> None:
        # start display
        if self.hasDisplay:
            _thread.start_new_thread(self.training, ())
            self.main.mainloop()

        else:
            self.training()

    def newGame(self) -> Game:
        return Game(
            DirectionAgent(POS.PACMAN, REP.PACMAN),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent(),
        )

    # ===== main training function =====
    def training(self) -> None:
        game: Game = self.newGame()
        game.pacman.setDir(self.mdpGetAction(game))

        ep = 0
        while ep < 10:
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            # enable display
            if self.hasDisplay:
                self.display.rerender()
                time.sleep(0.01)

            # reset when gameover
            if gameover or won:
                ep += 1

                game = self.newGame()
                self.display.newGame(game)

            game.pacman.setDir(self.mdpGetAction(game))

        

    def mdpGetAction(self, game: Game) -> int:
        # get reward grid
        rewardGrid: List[List[float]] = self.makeRewardGrid(game)

        # perform value iteration
        utilities: List[List[float]] = createGameSizeGrid(0)
        for i in range(self.maxIter):
            utilities, stable = self.bellmanUpdate(utilities, rewardGrid, game)

            if stable:
                break

        # get optimal action
        return np.argmax(self.getUtilValues(utilities, game, game.pacman.pos))

    # create reward grid from state space
    def makeRewardGrid(self, game: Game) -> List[List[float]]:
        # iniialise reward grid
        rewardGrid: List[List[float]] = createGameSizeGrid()

        # set power pellet reward
        for key, pwrplt in game.pwrplts.items():
            if pwrplt.valid:
                avgGhostDist: float = 1
                for ghost in game.ghostList:
                    if not ghost.isDead:
                        avgGhostDist += pwrplt.pos.manDist(ghost.pos)

                avgGhostDist /= len(game.ghostList)

                rewardGrid[pwrplt.pos.row][pwrplt.pos.col] = self.rewards["pwrplt"] * (1 / avgGhostDist**2)

        # set pellet reward
        for key, pellet in game.pellets.items():
            if pellet.valid:
                rewardGrid[pellet.pos.row][pellet.pos.col] = self.rewards["pellet"] * (
                    BOARD.TOTAL_PELLET_COUNT - game.pelletProgress
                )

        # set ghost reward
        for ghost in game.ghostList:
            if not ghost.isDead:
                if ghost.isFrightened:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = (
                        self.rewards["kill"] * game.pwrpltEffectCounter / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT
                    )
                else:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = self.rewards["death"]

        return rewardGrid

    # bellman update for value iterations
    def bellmanUpdate(
        self,
        utilities: List[List[float]],
        rewards: List[List[float]],
        game: Game,
    ) -> Tuple[List[List[float]], bool]:
        # initialise new utility value grid
        newUtils: List[List[float]] = createGameSizeGrid[0]

        # stable indicator
        stable = True

        # get new utility values
        for i, row in enumerate(game.state):
            for j, cell in enumerate(row):
                if not cell.isWall:
                    newUtils[i][j] = rewards[i][j] + self.gamma * max(self.getUtilValues(utilities, game, cell.coords))

                    if abs(newUtils[i][j] - utilities[i][j]) > self.epsilon:
                        stable = False

        return newUtils, stable

    # get utility value of neighbours
    def getUtilValues(self, utilities: List[List[float]], game: Game, pos: CPair):
        adjVals: List[float] = [float("-inf"), float("-inf"), float("-inf"), float("-inf")]

        for action, neighbour in game.getCell(pos).adj.items():
            if not neighbour is None:
                adjVals[action] = utilities[neighbour.coords.row][neighbour.coords.col]

        return adjVals


if __name__ == "__main__":
    training: MDPGuidedTraining = MDPGuidedTraining(
        {
            "mdpConfig": {
                "maxIterations": 200,
                "gamma": 0.75,
                "epsilon": 0.005,
            },
            "rewards": {
                "timestep": -1,
                "pellet": 5,
                "pwrplt": 200,
                "ghost": -50,
                "kill": 20,
            },
        },
        False,
    )
    training.start()
