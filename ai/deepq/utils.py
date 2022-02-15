from typing import List
import numpy as np

from ai.deepq.adam import Adam
from ai.deepq.neuralnet import NeuralNet


class NNUtils:
    def optimiseNN(self, tN: NeuralNet, cN: NeuralNet, replays: List[object], discount: float, tau: float, adam: Adam):
        # explode replays into separate lists
        s, a, r, t, nS = map(list, zip(*replays))

        s = np.concatenate(s)
        r = np.array(r)
        t = np.array(t)
        nS = np.concatenate(nS)
        batchSize = s.shape[0]

        # get TD error of network from replays
        tdError = NNUtils.getTDError(tN, cN, s, a, r, t, nS, discount, tau)

        # create delta matrix for batch td update
        indices = np.arange(batchSize)

        deltaMatrix = np.zeros((batchSize, tN.outSize))
        deltaMatrix[indices, a] = tdError

        # perform td update on target network
        tdUpdate = NNUtils.getTDUpdate(tN, s, deltaMatrix)

        # pass td update to adam optimiser to get a new set of values for the target network
        tN.setVals(adam.updateValues(tN.getVals(), tdUpdate))

    def getTDError(tN: NeuralNet, cN: NeuralNet, s, a, r, t, nS, discount: float, tau: float):
        nextQVals = cN.getActionValues(nS)
        probsVals = NNUtils.softmax(nextQVals, tau)

        vNVector = np.sum(nextQVals * probsVals, axis=1) * (1 - t)

        targetVector = r + discount * vNVector

        curQVals = tN.getActionValues(s)
        indices = np.arange(curQVals.shape[0])
        qVector = curQVals[indices, a]

        return targetVector - qVector

    def getTDUpdate(tN: NeuralNet, s, deltaMatrix: List[List[float]]):
        layers = len(tN.vals)
        bS = s.shape[0]
        tdUpdate = [dict() for i in range(layers)]

        inputs = [s]
        dxS = []
        for i in range(layers):
            w, b = tN.vals[i]["W"], tN.vals[i]["b"]

            prod = np.dot(inputs[i], w) + b
            inputs.append(np.maximum(prod, 0))

            dxS.append((prod > 0).astype(float))

        vS = [None for i in range(layers)]
        vS[layers - 1] = deltaMatrix
        for i in range(layers - 2, -1, -1):
            vS[i] = np.dot(vS[i + 1], tN.vals[i + 1]["W"].T) * dxS[i]

        for i in range(layers):
            tdUpdate[i]["W"] = np.dot(inputs[i].T, vS[i]) * bS
            tdUpdate[i]["b"] = np.sum(vS[i], axis=0, keepdims=True) / bS

        return tdUpdate

    def softmax(qVals: List[float], tau: float) -> List[float]:
        pref = qVals / tau
        maxPref = np.max(pref, axis=1).reshape((-1, 1))

        ePref = np.exp(pref - maxPref)
        sumEPref = np.sum(ePref, axis=1)

        return (ePref / sumEPref.reshape((-1, 1))).squeeze()
