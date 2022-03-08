from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils

# load neural network from config json
def loadNeuralNet(parentFolder: str, prefix: str, index: int) -> NeuralNet:
    indicator: str = "ep"
    if parentFolder == "saves":
        indicator = "avgc"

    return NeuralNet.load("./{}/{}/rl_nnconf_{}{}.json".format(parentFolder, prefix, indicator, index))


# load genome from config json
def loadGenome(parentFolder: str, prefix: str, index: int) -> Genome:
    indicator: str = "ep"
    if parentFolder == "saves":
        indicator = "avgc"

    return GenomeUtils.load("./{}/{}/ga_nnconf_{}{}.json".format(parentFolder, prefix, indicator, index))
