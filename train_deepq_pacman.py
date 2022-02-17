from copy import deepcopy
from datetime import datetime
from random import random
from tkinter import Tk
from typing import List, Tuple
import _thread
import numpy as np
import os
import time
from agents.base import DirectionAgent

from ai.deepq.adam import Adam
from ai.deepq.neuralnet import NeuralNet
from ai.deepq.replaybuf import ReplayBuffer
from ai.deepq.utils import NNUtils
from agents.blinky import BlinkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from data.data import BOARD, POS, REP
from game.game import Game
from gui.display import Display
from utils.coordinate import CPair


class DeepQLTraining:
    def __init__(self, trainingConfig: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("NEAT Training")

            self.display: Display = Display(self.main)

        # setup neural network
        self.network: NeuralNet = NeuralNet(trainingConfig["nnConfig"])

        # random state for softmax policy
        self.rand = np.random.RandomState()

        # setup optimiser
        self.adam: Adam = Adam(self.network.lDim, trainingConfig["adamConfig"])

        # setup replay buffer
        self.replayBuff: ReplayBuffer = ReplayBuffer(trainingConfig["replayConfig"])
        self.replayCount: int = trainingConfig["replayConfig"]["updatePerStep"]

        # setup hyperparameters
        self.gamma: float = trainingConfig["gamma"]
        self.tau: float = trainingConfig["tau"]

        # previous state and actions
        self.pState: List[List[int]] = None
        self.pAction: int = None

        # simluation config
        self.simCap: int = trainingConfig["simulationCap"]

        # training status
        self.rSum: float = 0
        self.epSteps: int = 0

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
            BlinkyClassicAgent(),
            InkyClassicAgent(),
            ClydeClassicAgent(),
            PinkyClassicAgent(),
            enableGhost=True,
            enablePwrPlt=True,
        )

    # ===== main training function =====
    def training(self) -> None:
        game: Game = self.newGame()
        if self.hasDisplay:
            self.display.newGame(game)

        action: int = self.agentInit(self.processState(game))
        game.pacman.setDir(action)

        eps: int = 0
        while eps < self.simCap:
            gameover, won, atePellet = game.nextStep()

            # enable display
            if self.hasDisplay:
                self.display.rerender(atePellet)
                time.sleep(0.01)

            if gameover:
                if won:
                    self.agentEnd(1000)
                else:
                    self.agentEnd(-1000)

                eps += 1

                print("ep{}: r{} | e{}".format(eps, self.rSum, self.epSteps))

                game = self.newGame()
                if self.hasDisplay:
                    self.display.newGame(game)

                action = self.agentInit(self.processState(game))
                game.pacman.setDir(action)

            else:
                reward: int = -1

                if atePellet:
                    reward = 10

                action = self.agentStep(self.processState(game), reward)
                game.pacman.setDir(action)
                            

    # ===== auxiliary training functions =====
    def processState(self, game: Game) -> List[int]:
        rt: List[int] = []

        pacPos: CPair = game.pacman.pos        
        pRow, pCol, = pacPos.row, pacPos.col

        # valid actions
        for pos in pacPos.getNeighbours(True):
            rt.append(int(hasattr(pos, "row")))
            
        # ghost data
        for ghost in game.ghosts:
            gRow, gCol = ghost.pos.row, ghost.pos.col
            rt.append(pRow - gRow)
            rt.append(pCol - gCol)
            rt.append(int(ghost.isDead))
            rt.append(int(ghost.isFrightened))

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

    # softmax policy for probabilistic action selection
    def policy(self, state: List[int]):
        return self.rand.choice(
            a=self.network.outSize,
            p=NNUtils.softmax(
                self.network.predict(state),
                self.tau,
            ).squeeze(),
        )

    # episode initialisation
    def agentInit(self, state: List[int]) -> int:
        self.pState = np.array([state])
        self.pAction = self.policy(self.pState)

        # reset training status
        self.rSum = 0
        self.epSteps = 0

        return self.pAction

    # episode step
    def agentStep(self, state: List[int], reward: float) -> int:
        # perform next step
        state: List[List[int]] = np.array([state])
        action = self.policy(state)

        # update replay buffer
        self.replayBuff.append(self.pState, self.pAction, reward, 0, state)

        # perform update if replay buffer is ready
        if self.replayBuff.isReady():
            cN = deepcopy(self.network)
            for i in range(self.replayCount):
                NNUtils.optimiseNN(self.network, cN, self.replayBuff.getSample(), self.gamma, self.tau, self.adam)

        # update previous state and action
        self.pState = state
        self.pAction = action

        # update training status
        self.rSum += reward
        self.epSteps += 1

        return action

    # episode termination
    def agentEnd(self, reward: float):
        # update replay buffer
        self.replayBuff.append(self.pState, self.pAction, reward, 1, np.zeros_like(self.pState))

        # perform update if replay buffer is ready
        if self.replayBuff.isReady():
            cN = deepcopy(self.network)
            for i in range(self.replayCount):
                NNUtils.optimiseNN(self.network, cN, self.replayBuff.getSample(), self.gamma, self.tau, self.adam)

        # update training status
        self.rSum += reward
        self.epSteps += 1


if __name__ == "__main__":
    training: DeepQLTraining = DeepQLTraining(
        {
            "adamConfig": {
                "stepSize": 1e-3,
                "bM": 0.9,
                "bV": 0.999,
                "epsilon": 0.001,
            },
            "gamma": 0.95,
            "nnConfig": {
                "inSize": 23,
                "hidden": [
                    256,
                    16,
                    16,
                ],
                "outSize": 4,
            },
            "replayConfig": {
                "rbSize": 50000,
                "batchSize": 8,
                "updatePerStep": 4,
            },
            "simulationCap": 100,
            "simulationConfig": {
                "ghost": True,
                "pwrplt": False,
            },
            "tau": 0.001,
        },
        True,
    )
    training.start()
