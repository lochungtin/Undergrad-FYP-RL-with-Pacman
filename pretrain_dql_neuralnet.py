from math import floor
import os
from random import shuffle
from typing import List, Tuple
import json
import numpy as np

from ai.deepq.adam import Adam
from ai.deepq.neuralnet import NeuralNet
from ai.deepq.utils import NNUtils


# load examples from file
def loadFile(ep: int) -> List[List[float]]:
    rt: List[List[float]] = []

    with open("./out/PACMAN_MDP_EX/run{}.txt".format(ep), "r") as file:
        for line in file:
            rt.append(json.loads(line))

    return rt


# split loaded data into mini batches
def makeBatches(data: List[List[float]]) -> Tuple[List[List[List[float]]], List[List[int]]]:
    # shuffle data
    shuffle(data)

    # store
    stateSplt: List[List[List[float]]] = []
    targetSplt: List[List[int]] = []

    for splt in np.array_split(data, floor(len(data) / 8)):
        stateBatchSplt: List[List[float]] = []
        targetBatchSplt: List[int] = []

        # split data
        for line in splt[0:8]:
            stateBatchSplt.append(line[0:23])

            targetVec = [0, 0, 0, 0]
            targetVec[int(line[23])] = 1

            targetBatchSplt.append(targetVec)

        stateSplt.append(stateBatchSplt)
        targetSplt.append(targetBatchSplt)

    return np.array(stateSplt), np.array(targetSplt)


def main(config: dict[str, object]):
    # create network
    net: NeuralNet = NeuralNet(config["nnConfig"])

    # create optimiser
    adam: Adam = Adam(net.lDim, config["adamConfig"])

    # train neural network
    for i in range(1000):
        # load data and split into batches
        stateSplt, targetSplt = makeBatches(loadFile(i))

        # fit network
        for j in range(len(stateSplt)):
            print("Batch: {}".format(i * 8 + j))

            update = NNUtils.backpropagation(net, stateSplt[j], targetSplt[j])
            net.setVals(adam.updateVals(net.getVals(), update))

    # save network
    os.mkdir("./out/PACMAN_DQL_PRE")
    net.save(i * 8 + j + 1, "PACMAN_DQL_PRE")


if __name__ == "__main__":
    config: dict[str, object] = {
        "nnConfig": {
            "inSize": 23,
            "hidden": [
                256,
                16,
                4,
            ],
            "outSize": 4,
        },
        "adamConfig": {
            "stepSize": 1e-3,
            "bM": 0.9,
            "bV": 0.999,
            "epsilon": 0.1,
            "decay": 0.9999,
            "decayMax": 0.001,
        },
    }
    main(config)
