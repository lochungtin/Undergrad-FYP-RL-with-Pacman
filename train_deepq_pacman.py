from copy import deepcopy
from datetime import datetime
from random import random
from tkinter import Tk
from typing import List, Tuple
import _thread
import os
import time

from ai.deepq.adam import Adam
from ai.deepq.neuralnet import NeuralNet
from ai.deepq.replaybuf import ReplayBuffer
from game.paiv import PAIV
from gui.display import Display


class DeepQRLTraining:
    def __init__(self, trainingConfig: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("NEAT Training")

            self.display: Display = Display(self.main)

        # setup neural network
        self.network: NeuralNet = NeuralNet(trainingConfig["nnConfig"])

        # setup optimiser
        self.adam: Adam = Adam(self.network.lDim, trainingConfig["adamConfig"])

        # setup replay buffer
        self.replayBuff: ReplayBuffer = ReplayBuffer(trainingConfig["replayConfig"])

        # setup hyperparameters
        self.gamma: float = trainingConfig["gamma"]
        self.tau: float = trainingConfig["tau"]

        # previous state and actions
        self.pState: List[int] = None
        self.pAction: int = None

        # training status
        self.rewardSum: float = 0
        self.epSteps: int = 0


if __name__ == "__main__":
    for _ in range(50):
        training: DeepQRLTraining = DeepQRLTraining(
            {
                "adamConfig": {
                    "stepSize": 1e-3,
                    "bM": 0.9,
                    "bV": 0.999,
                    "epsilon": 0.001,
                },
                "nnConfig": {
                    "inSize": 37,
                    "hidden": [256, 16, 16,],
                    "outSize": 4,
                },
                "replayConfig": {
                    "rbSize": 50000,
                    "batchSize": 8,
                    "updatePerStep": 4,
                },
                "gamma": 0.95,
                "tau": 0.001
            },
            False,
        )
        training.start()
