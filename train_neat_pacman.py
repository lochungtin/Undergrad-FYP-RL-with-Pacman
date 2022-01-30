from copy import deepcopy
from math import ceil, floor
from multiprocessing.connection import wait
from random import choices, random
from tkinter import Tk
from typing import List, Tuple
import _thread
import time

from numpy import empty

from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils
from game.paiv import PAIV
from gui.display import Display


class NEATTraining:
    def __init__(
        self, trainingConfig: dict[str, object], hasDisplay: bool = False
    ) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("NEAT Training")

            self.display: Display = Display(self.main)

        # simulation config
        self.enableGhost: bool = trainingConfig["simulationConfig"]["ghost"]
        self.enablePwrPlt: bool = trainingConfig["simulationConfig"]["pwrplt"]

        # training config
        self.popSize: int = trainingConfig["populationSize"]
        self.selSize: int = trainingConfig["selectionSize"]
        self.genCap: int = trainingConfig["generationCap"]

        # genome config
        self.gConf: dict[str, int] = trainingConfig["genomeConfig"]

        # distance compatibility config
        self.cConf: dict[str, float] = trainingConfig["comp"]

        # fitness coefficent
        self.fCoef: dict[str, int] = trainingConfig["fitnessCoeff"]

        # mutation probabilities
        self.mProb: dict[str, float] = trainingConfig["mutationConfig"]

        # crossing option
        self.cOpt: int = trainingConfig["crossOpt"]

        # generations per genome saving
        self.saving: int = trainingConfig["saveOpt"]

    # create mutation config
    def mutationConfig(self) -> dict[str, bool]:
        return {
            "addNode": random() < self.mProb["addNode"],
            "addConn": random() < self.mProb["addConn"],
            "mutBias": random() < self.mProb["mutBias"],
            "mutWeight": random() < self.mProb["mutWeight"],
            "mutConn": random() < self.mProb["mutConn"],
        }

    # run genome against simluation and get fitness value
    def runSim(self, genome: Genome) -> float:
        game: PAIV = PAIV(genome, self.enableGhost, self.enablePwrPlt)

        if self.hasDisplay:
            self.display.newGame(game)

        pelletCount: int = 0
        emptyStep: int = 0
        gameover: bool = False
        won: bool = False
        while game.pelletDrought < 50 and not gameover and not won:
            gameover, won, atePellet = game.nextStep()

            # enable display
            if self.hasDisplay:
                self.display.rerender(atePellet)
                time.sleep(0.01)

            if atePellet:
                pelletCount += 1
            else:
                emptyStep += 1

        fitness: float = (
            self.fCoef["p"] * pelletCount
            + self.fCoef["e"] * emptyStep
            + self.fCoef["i"] * game.invalidSteps
            + self.fCoef["w"] * won
            + self.fCoef["l"] * (gameover or game.pelletDrought >= 45)
        )

        return fitness

    # start training (main function)
    def start(self) -> None:
        # start display
        if self.hasDisplay:
            _thread.start_new_thread(self.evolution, ())
            self.main.mainloop()

        else:
            self.evolution()

    # start neuro evolution
    def evolution(self) -> None:
        # create population
        pop: List[Genome] = [Genome(self.gConf, True) for _ in range(self.popSize)]

        # innovation number map
        innovMap: dict[str, int] = {}
        for i in range(self.gConf["inSize"]):
            for o in range(
                self.gConf["inSize"],
                self.gConf["outSize"] + self.gConf["inSize"],
            ):
                key: str = Genome.genInnovKey(0, 1, i, o)
                innovMap[key] = i * self.gConf["outSize"] + (o - self.gConf["inSize"])
        innovMap["SIZE"] = len(innovMap)

        # filenames of saved config
        configSaves: List[str] = []

        # initial mutation
        for i, genome in enumerate(pop):
            pop[i] = genome.mutate(self.mutationConfig(), innovMap)

        bestScore: float = float("-inf")

        # evolution process
        for gen in range(self.genCap):
            # evaluate population perfomance
            perf: List[Tuple[int, float]] = []
            for i, genome in enumerate(pop):
                # run simulation
                fitness: float = self.runSim(genome)

                # adjust fitness to topology
                fitness /= GenomeUtils.fitnessAdj(genome, pop, self.cConf)

                if fitness > bestScore:
                    bestScore = fitness

                print(
                    "Gen: {}\tgenome: {}\tfitness: {}\tbest:{}".format(
                        gen, i, fitness, bestScore
                    )
                )

                # save fitness value
                perf.append((i, fitness))

            # get top performing genomes
            perf = sorted(perf, key=lambda p: p[1], reverse=True)[: self.selSize]
            tGenomes: List[Genome] = [deepcopy(pop[p[0]]) for p in perf]

            # save genome config every N generations
            if gen % self.saving == 0 and gen != 0:
                configSaves.append(GenomeUtils.save(tGenomes[0], gen))

            # exit evoluation loop if end
            if gen + 1 == self.genCap:
                break

            # mutate and cross top genomes
            size: int = len(tGenomes)
            for i in range(self.popSize):
                if i < self.popSize / 3:
                    pop[i] = tGenomes[i % size].mutate(
                        self.mutationConfig(), innovMap
                    )
                else:
                    cycle: int = i % (self.selSize - 1)
                    p1: Genome = tGenomes[cycle]
                    p2: Genome = tGenomes[cycle + 1]
                    pop[i] = GenomeUtils.cross(p1, p2, self.cOpt)

        # save best performing genome after training process
        # get best performing genome
        configSaves.append(GenomeUtils.save(tGenomes[0], self.genCap))


if __name__ == "__main__":
    training: NEATTraining = NEATTraining(
        {
            "comp": {
                "cD": 1,
                "cE": 1,
                "cW": 1,
                "dThres": 0.4,
            },
            "crossOpt": GenomeUtils.CROSS_OPTIONS["MAX"],
            "fitnessCoeff": {
                "p": 5,
                "e": -5,
                "i": -10,
                "w": 1000,
                "l": -1000,
            },
            "generationCap": 300,
            "genomeConfig": {
                "inSize": 37,
                "outSize": 4,
            },
            "mutationConfig": {
                "addNode": 0.1,
                "addConn": 0.7,
                "mutBias": 0.4,
                "mutWeight": 0.8, 
                "mutConn": 0.5,
            },
            "populationSize": 100,
            "saveOpt": 25,
            "selectionSize": 15,
            "simulationConfig": {
                "ghost": False,
                "pwrplt": False,
            },
        },
        False,
    )
    training.start()
