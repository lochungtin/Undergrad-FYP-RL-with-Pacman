from math import floor
from random import shuffle
from typing import List, Tuple
import json
import numpy as np
import os

from ai.deepq.adam import Adam
from ai.deepq.neuralnet import NeuralNet
from ai.deepq.utils import NNUtils


# load examples from file
def loadFile(ep: int) -> List[List[float]]:
    rt: List[List[float]] = []

    with open("./out/BLINKY_MDP_EX/run{}.txt".format(ep), "r") as file:
        for line in file:
            rt.append(json.loads(line))

    return rt


# split loaded data into mini batches
def makeBatches(
    data: List[List[float]], batchSize: int, inSize: int
) -> Tuple[List[List[List[float]]], List[List[int]]]:
    # shuffle data
    shuffle(data)

    # store
    stateSplt: List[List[List[float]]] = []
    targetSplt: List[List[int]] = []

    for splt in np.array_split(data, floor(len(data) / batchSize)):
        stateBatchSplt: List[List[float]] = []
        targetBatchSplt: List[int] = []

        # split data
        for line in splt[0:batchSize]:
            stateBatchSplt.append(line[0:inSize])

            targetVec = [0, 0, 0, 0]
            targetVec[int(line[inSize])] = 1

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
    for i in range(431):
        # load data and split into batches
        stateSplt, targetSplt = makeBatches(loadFile(i), config["batchSize"], config["nnConfig"]["inSize"])

        # fit network
        for j in range(len(stateSplt)):
            print("Batch: {}".format(i * config["batchSize"] + j))

            update = NNUtils.backpropagation(net, stateSplt[j], targetSplt[j])
            net.setVals(adam.updateVals(net.getVals(), update))

    # save network
    os.mkdir("./out/BLINKY_DQL_PRE")
    NNUtils.save(net, i * config["batchSize"] + j + 1, "BLINKY_DQL_PRE")


if __name__ == "__main__":
    config: dict[str, object] = {
        "adamConfig": {
            "stepSize": 1e-3,
            "bM": 0.9,
            "bV": 0.999,
            "epsilon": 0.1,
        },
        "batchSize": 8,
        "nnConfig": {
            "inSize": 15,
            "hidden": [
                256,
                16,
                4,
            ],
            "outSize": 4,
        },
    }
    main(config)
