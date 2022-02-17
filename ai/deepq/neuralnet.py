from __future__ import annotations
from copy import deepcopy
from typing import List
import json
import numpy as np

from ai.predictable import Predictable


class NeuralNet(Predictable):
    def __init__(self, config: dict[str, object]) -> None:
        if config != None:
            self.inSize: int = config["inSize"]
            self.outSize: int = config["outSize"]

            self.lDim: List[int] = deepcopy(config["hidden"])
            self.lDim.insert(0, self.inSize)
            self.lDim.append(self.outSize)

            # initialise weights and biases
            self.vals: List[dict[str, object]] = [dict() for i in range(len(self.lDim) - 1)]
            for i in range(len(self.lDim) - 1):
                self.vals[i]["W"] = self.genWeights(self.lDim[i], self.lDim[i + 1])
                self.vals[i]["b"] = np.zeros((1, self.lDim[i + 1]))

    def genWeights(self, inCount: int, outCount: int) -> List[List[float]]:
        # create weight matrix
        tensor = np.random.RandomState().normal(0, 1, (inCount, outCount))

        # normalise weights to [0, 1]
        if inCount < outCount:
            tensor = tensor.T

        tensor, r = np.linalg.qr(tensor)
        d = np.diag(r, 0)
        ph = np.sign(d)
        tensor *= ph

        if inCount < outCount:
            tensor = tensor.T

        return tensor

    def predict(self, input: List[List[int]]) -> List[float]:
        layers = len(self.vals) - 1
        x = input
        for i in range(layers):
            w, b = self.vals[i]["W"], self.vals[i]["b"]
            psi = np.dot(x, w) + b

            # relu
            x = np.maximum(psi, 0)

        w, b = self.vals[layers]["W"], self.vals[layers]["b"]
        q_vals = np.dot(x, w) + b

        return q_vals

    def getVals(self):
        return deepcopy(self.vals)

    def setVals(self, vals: List[dict[str, object]]):
        self.vals = deepcopy(vals)

    # save and load NN config
    def save(self, epCount: int, runPref: str, parentFolder: str = "out"):
        vals = deepcopy(self.vals)

        for i in vals:
            i["W"] = i["W"].tolist()
            i["b"] = i["b"].tolist()

        filename: str = "./{}/{}/rl_nnconf_ep{}.json".format(parentFolder, runPref, epCount)
        with open(filename, "w+") as outfile:
            json.dump({"inSize": self.inSize, "outSize": self.outSize, "lDim": self.lDim, "vals": vals}, outfile)

    def load(filename: str) -> NeuralNet:
        with open(filename, "r") as inFile:
            data: dict[str, object] = json.load(inFile)

            net = NeuralNet(None)

            net.inSize = data["inSize"]
            net.outSize = data["outSize"]
            net.lDim = data["lDim"]

            for i in data["vals"]:
                i["W"] = np.array(i["W"])
                i["b"] = np.array(i["b"])

            net.vals = data["vals"]

            return net
