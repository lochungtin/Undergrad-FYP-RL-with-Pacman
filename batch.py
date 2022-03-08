from math import floor
from typing import List, Tuple
import os

from ai.deepq.neuralnet import NeuralNet
from data.data import GHOST_CLASS_TYPE
from game.game import Game
from utils.game import newGame
from utils.printer import printPacmanPerfomance


class BatchAutoApp:
    def __init__(self, appConfig: dict[str, object]) -> None:
        # game config
        self.ghosts: dict[str, int] = appConfig["ghosts"]
        self.enablePwrPlt: bool = appConfig["enablePwrPlt"]

        # neural net
        self.neuralnets: dict[str, str] = appConfig["neuralnets"]

        # genomes
        self.genomes: dict[str, str] = appConfig["genomes"]

        # training target
        self.target: str = appConfig["targetAgent"]

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
        # create new game
        self.neuralnets[self.target] = net
        game: Game = newGame(self.ghosts, self.enablePwrPlt, self.neuralnets, self.genomes)

        # run game
        while True:
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            if gameover or won:
                return printPacmanPerfomance(0, game, False)

            if game.timesteps > 1000:
                break

        return 0


if __name__ == "__main__":
    app: BatchAutoApp = BatchAutoApp(
        {
            "enablePwrPlt": True,
            "genomes": {},
            "ghosts": {
                "blinky": GHOST_CLASS_TYPE.OGNL,
                "inky": GHOST_CLASS_TYPE.NONE,
                "clyde": GHOST_CLASS_TYPE.NONE,
                "pinky": GHOST_CLASS_TYPE.OGNL,
            },
            "iteration": {
                "filter": 20,
                "performance": 100,
            },
            "neuralnets": {},
            "runPref": "RL0703_2107",
            "threshold": {
                "completion": 70,
                "percentile": 0.1,
            },
        }
    )

    app.start()
