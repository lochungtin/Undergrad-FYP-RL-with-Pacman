from math import log2
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

        # training config
        self.gameCap: int = trainingConfig["gameCap"]

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
        ep: int = 0

        # create new game
        game: Game = self.newGame()
        if self.hasDisplay:
            self.display.newGame(game)

        # create new save file for new run
        open("./out/DG_DQL_EX/run{}.txt".format(ep), "x")

        while True:
            # get action
            action: int = self.mdpGetAction(game)

            # get features and append action
            features: List[float] = pacmanFeatureExtraction(game)
            features.append(action)

            # save array
            runFile = open("./out/DG_DQL_EX/run{}.txt".format(ep), "a")
            runFile.write(str(features) + "\n")
            runFile.close()

            # set action and perform next step
            game.pacman.setDir(action)
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            # rerender display if enabled
            if self.hasDisplay:
                self.display.rerender()

            # reset game when gameover
            if gameover or won:
                self.printPerformance(ep, game)

                # exit loop
                ep += 1
                if ep >= self.gameCap:
                    break

                # create new game
                game = self.newGame()
                if self.hasDisplay:
                    self.display.newGame(game)

                # create new save file for new run
                open("./out/DG_DQL_EX/run{}.txt".format(ep), "x")

    def printPerformance(self, ep: int, game: Game) -> None:
        consumption: int = 68 - game.pelletProgress
        print(
            "ep: {}\tt: {}\tl: {}\tc: {}/68 = {}%".format(
                ep,
                game.timesteps,
                game.pelletProgress,
                consumption,
                round(consumption / 68 * 100, 2),
            )
        )

    # ===== MDP solver =====
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

    # ===== auxiliary functions =====
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
            "gameCap": 1000,
            "mdpConfig": {
                "maxIterations": 10000,
                "gamma": 0.90,
                "epsilon": 0.00005,
            },
            "rewards": {
                "timestep": -0.05,
                "pellet": 5,
                "pwrplt": 2,
                "ghost": -100,
                "kill": 30,
            },
        },
        False,
    )
    training.start()
