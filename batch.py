from copy import deepcopy
from math import floor
from typing import List, Tuple
import os

from agents.base import GhostAgent
from agents.blinky import BlinkyClassicAgent
from agents.inky import InkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.pacman import PacmanDQLAgent
from agents.pinky import PinkyClassicAgent
from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils
from game.game import Game
from utils.printer import printPacmanPerfomance


# load neural network from config json
def loadNeuralNet(parentFolder: str, prefix: str, ep: int) -> NeuralNet:
    return NeuralNet.load("./{}/{}/rl_nnconf_ep{}.json".format(parentFolder, prefix, ep))


# load genome from config json
def loadGenome(parentFolder: str, prefix: str, gen: int) -> Genome:
    return GenomeUtils.load("./{}/{}/ga_nnconf_ep{}.json".format(parentFolder, prefix, gen))


class BatchAutoApp:
    def __init__(self, appConfig: dict[str, object]) -> None:
        # ghost agent config
        self.ghosts: dict[str, GhostAgent] = appConfig["ghosts"]

        # directory path
        self.path: str = "./out/{}".format(appConfig["runPref"])

        # iteration counts
        self.filterItr: int = appConfig["iteration"]["filter"]
        self.performanceItr: int = appConfig["iteration"]["performance"]

        # threshold values
        self.cThreshold: float = appConfig["threshold"]["completion"]
        self.pThreshold: float = appConfig["threshold"]["percentile"]

    def start(self) -> None:
        # first pass general filtering
        filter: List[Tuple[str, int]] = self.filter()
        print(filter)

        # second pass percentile filtering
        percentile: List[str] = self.getTopPercentile(filter)
        print(percentile)

        # get average score
        avg: dict[str, float] = self.getAverages(percentile)
        print(avg)

    # get neural network configs that has once pass the first threshold for completion
    def filter(self) -> List[Tuple[str, int]]:
        filter: dict[str, int] = {}

        for i in range(self.filterItr):
            print("Filter Stage - Iteration: {}".format(i))
            for file in os.listdir(self.path):
                if self.runGame(NeuralNet.load("{}/{}".format(self.path, file))) > self.cThreshold:
                    if not file in filter:
                        filter[file] = 0

                    filter[file] += 1

        return filter

    # get top n percentile of the filtered based on number of appearances
    def getTopPercentile(self, filter: dict[str, int]) -> List[str]:
        results: List[Tuple[str, int]] = [(file, res) for file, res in filter.items()]
        results.sort(key=lambda p: p[1], reverse=True)

        return list(map(lambda p: p[0], results[0 : floor(len(results) * self.pThreshold)]))

    # get average score of top neural network configs
    def getAverages(self, topFiles: List[str]) -> dict[str, float]:
        averages: dict[str, float] = {}

        for file in topFiles:
            print("Performance Stage - Filename: {}".format(file))
            average: float = 0
            for i in range(self.performanceItr):
                average += self.runGame(NeuralNet.load("{}/{}".format(self.path, file)))

            averages[file] = average / self.performanceItr

        return averages

    # run game
    def runGame(self, net: NeuralNet) -> float:
        ghosts: dict[str, GhostAgent] = deepcopy(self.ghosts)
        game: Game = Game(
            pacman=PacmanDQLAgent(net),
            blinky=ghosts["blinky"],
            inky=ghosts["inky"],
            clyde=ghosts["clyde"],
            pinky=ghosts["pinky"],
        )

        kills: int = 0
        stationary: int = 0

        while True:
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            if ateGhost:
                kills += 1

            if not game.pacman.moved:
                stationary += 1

            if gameover or won:
                return printPacmanPerfomance(0, game, False)

            if game.timesteps > 1000:
                break

        return 0


if __name__ == "__main__":
    app: BatchAutoApp = BatchAutoApp(
        {
            "ghosts": {
                "blinky": BlinkyClassicAgent(),
                "inky": None,
                "clyde": None,
                "pinky": PinkyClassicAgent(),
            },
            "iteration": {
                "filter": 20,
                "performance": 100,
            },
            "runPref": "RL0703_2107",
            "threshold": {
                "completion": 70,
                "percentile": 0.1,
            },
        }
    )

    app.start()
