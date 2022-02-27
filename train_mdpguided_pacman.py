from math import log2
from copy import deepcopy
from tkinter import Tk
from typing import List, Tuple
import _thread
import numpy as np

from agents.base import DirectionAgent
from agents.pacman import pacmanFeatureExtraction
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
        self.gamma: float = trainingConfig["mdpConfig"]["gamma"]
        self.epsilon: float = trainingConfig["mdpConfig"]["epsilon"]

        self.maxIter: int = trainingConfig["mdpConfig"]["maxIterations"]

        # reward constants
        self.rewards: dict[str, float] = trainingConfig["rewards"]

        # game object
        self.newGame()

    # start training (main function)
    def start(self) -> None:
        # start display
        if self.hasDisplay:
            _thread.start_new_thread(self.training, ())
            self.main.mainloop()

        else:
            self.training()

    def newGame(self):
        self.game = Game(
            DirectionAgent(POS.PACMAN, REP.PACMAN),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent(),
            enablePwrPlt=True,
        )

    # ===== main training function =====
    def training(self) -> None:
        if self.hasDisplay:
            self.display.newGame(self.game)

        ep = 0
        while ep < 1:
            self.game.pacman.setDir(self.mdpGetAction(self.game))
            gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()

            # enable display
            if self.hasDisplay:
                self.display.rerender()

            # reset when gameover
            if gameover or won:
                ep += 1

                consumption: int = 68 - self.game.pelletProgress
                print(
                    "l: {}\tc: {}/68 = {}%".format(
                        self.game.pelletProgress, consumption, round(consumption / 68 * 100, 2)
                    )
                )

                if self.hasDisplay:
                    self.display.newGame(self.game)

    # get optimal action
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
        rewardGrid: List[List[float]] = createGameSizeGrid(self.rewards["timestep"])

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
                rewardGrid[pellet.pos.row][pellet.pos.col] = self.rewards["pellet"] * log2(
                    BOARD.TOTAL_PELLET_COUNT - game.pelletProgress + 1
                )

        # set ghost reward
        for ghost in game.ghostList:
            if not ghost.isDead:
                if ghost.isFrightened:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = (
                        self.rewards["kill"] * game.pwrpltEffectCounter / GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT
                    )
                else:
                    rewardGrid[ghost.pos.row][ghost.pos.col] = self.rewards["ghost"]

        return rewardGrid

    # bellman update for value iterations
    def bellmanUpdate(
        self,
        utilities: List[List[float]],
        rewards: List[List[float]],
        game: Game,
    ) -> Tuple[List[List[float]], bool]:
        # initialise new utility value grid
        newUtils: List[List[float]] = createGameSizeGrid(0)

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
                "maxIterations": 10000,
                "gamma": 0.90,
                "epsilon": 0.00005,
            },
            "rewards": {
                "timestep": -0.05,
                "pellet": 5,
                "pwrplt": 2,
                "ghost": -1000,
                "kill": 30,
            },
        },
        False,
    )
    training.start()
