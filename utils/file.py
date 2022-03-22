from typing import Tuple

from ai.deepq.neuralnet import NeuralNet
from ai.deepq.utils import NNUtils
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils

# load neural network from config json
def loadNeuralNetT(tuple: Tuple[str, str, int]) -> NeuralNet:
    return loadNeuralNet(tuple[0], tuple[1], tuple[2])


def loadNeuralNet(parentFolder: str, prefix: str, index: int) -> NeuralNet:
    indicator: str = "ep"
    if parentFolder == "saves":
        indicator = "avgc"

    return NNUtils.load("./{}/{}/rl_nnconf_{}{}.json".format(parentFolder, prefix, indicator, index))


# load genome from config json
def loadGenomeT(tuple: Tuple[str, str, int]) -> NeuralNet:
    return loadGenome(tuple[0], tuple[1], tuple[2])


def loadGenome(parentFolder: str, prefix: str, index: int) -> Genome:
    indicator: str = "ep"
    if parentFolder == "saves":
        indicator = "avgc"

    return GenomeUtils.load("./{}/{}/ga_nnconf_{}{}.json".format(parentFolder, prefix, indicator, index))
