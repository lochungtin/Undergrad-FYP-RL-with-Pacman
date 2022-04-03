from copy import deepcopy
from datetime import datetime
from random import random
from tkinter import Tk
from typing import List, Tuple
import _thread
import numpy as np
import os
import time

from agents.utils.features import ghostFeatureExtraction
from ai.neat.gene import ConnGene
from ai.neat.genome import Genome
from ai.neat.utils import GenomeUtils
from data.config import BOARD
from data.data import AGENT_CLASS_TYPE, REP
from game.game import Game, newGame
from gui.display import Display
from utils.printer import printPacmanPerfomance 


class NEATTraining:
    def __init__(self, config: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("NEAT Ghost Training")

            self.display: Display = Display(self.main)

        # training config
        self.popSize: int = config["populationSize"]
        self.selSize: int = config["selectionSize"]
        self.genCap: int = config["generationCap"]

        # genome config
        self.gConf: dict[str, int] = config["genomeConfig"]

        # distance compatibility config
        self.cConf: dict[str, float] = config["comp"]

        # fitness coefficent
        self.fCoef: dict[str, int] = config["fitnessCoeff"]

        # mutation probabilities
        self.mProb: dict[str, float] = config["mutationConfig"]

        # crossing option
        self.cOpt: int = config["crossOpt"]

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
    def runSim(self, genome: Genome, gen: int, index: int) -> float:
        game: Game = newGame(
            {
                REP.PACMAN: AGENT_CLASS_TYPE.SMDP,
                REP.BLINKY: AGENT_CLASS_TYPE.TRNG,
                "secondary": {
                    REP.INKY: AGENT_CLASS_TYPE.NONE,
                    REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                    REP.PINKY: AGENT_CLASS_TYPE.STTC,
                },
            },
            True,
            {},
            {},
        )

        if self.hasDisplay:
            self.display.newGame(game)

        lowestDist: int = float("inf")
        gameover: bool = False
        won: bool = False
        while not gameover and not won and game.timesteps < 200:
            # perform next step
            qVals: List[float] = genome.predict(ghostFeatureExtraction(game, REP.BLINKY))
            action: int = np.argmax(qVals)

            game.ghosts[REP.BLINKY].setDir(action)
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            # update shortest distance achieved
            dist: int = game.pacman.pos.manDist(game.ghosts[REP.BLINKY].pos)
            if dist < lowestDist:
                lowestDist = dist

            # enable display
            if self.hasDisplay:
                self.display.rerender()
                time.sleep(0.01)

        # print game performance
        printPacmanPerfomance("{}.{}".format(gen, index), game)

        fitness: float = (
            self.fCoef["lowestDistance"] * lowestDist
            + self.fCoef["pelletProgress"] * (BOARD.TOTAL_PELLET_COUNT - game.pelletProgress)
            + self.fCoef["loss"] * gameover
            + self.fCoef["won"] * won
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

    # ===== population creation =====
    # create fresh population
    def newPopulation(self) -> Tuple[List[Genome], dict[str, int]]:
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

        # initial mutation
        for i, genome in enumerate(pop):
            pop[i] = genome.mutate(self.mutationConfig(), innovMap)

        return pop, innovMap

    # load best genome and repopulate
    def loadPopulation(self, gFilename: str, iFilename: str) -> Tuple[List[Genome], dict[str, int]]:
        # load genome and innovMap from config file
        genome: Genome = GenomeUtils.load(gFilename, "milestones")
        innovMap: dict[str, int] = GenomeUtils.loadInnov(iFilename, "milestones")

        for (key, conn) in genome.conns.items():
            i, o = ConnGene.parseKey(key)
            innovKey = Genome.genInnovKey(genome.lMap[i], genome.lMap[o], i, o)
            conn.innov = innovMap[innovKey]

        # repopulate with mutation
        pop: List[Genome] = [deepcopy(genome).mutate(self.mutationConfig(), innovMap) for _ in range(self.popSize)]

        return pop, innovMap

    # ===== main evoluation function =====
    def evolution(self) -> None:
        runPref: str = "NE{}".format(datetime.now().strftime("%d%m_%H%M"))
        os.mkdir("out/{}".format(runPref))

        # initialise population and innovation map
        pop, innovMap = self.newPopulation()
        # pop, innovMap = self.loadPopulation("NP-NG_GENOME_GEN50.json", "NP-NG_INNOV_GEN50.json")

        # evolution process
        for gen in range(self.genCap):
            # evaluate population perfomance
            perf: List[Tuple[int, float]] = []
            for i, genome in enumerate(pop):
                # run simulation
                fitness = self.runSim(genome, gen, i)

                # adjust fitness to topology
                fitness /= GenomeUtils.fitnessAdj(genome, pop, self.cConf)              

                # save fitness value
                perf.append((i, fitness))

            # get top performing genomes
            perf = sorted(perf, key=lambda p: p[1], reverse=True)[: self.selSize]
            tGenomes: List[Genome] = [deepcopy(pop[p[0]]) for p in perf]

            # save genome config every N generations
            if gen % 20 == 0 and gen != 0:
                GenomeUtils.save(tGenomes[0], runPref, gen)
                GenomeUtils.saveInnov(innovMap, runPref, gen)

            # exit evoluation loop if end
            if gen + 1 == self.genCap:
                break

            # mutate and cross top genomes
            size: int = len(tGenomes)
            for i in range(self.popSize):
                if i < 2 * self.popSize / 3:
                    pop[i] = tGenomes[i % size].mutate(self.mutationConfig(), innovMap)
                else:
                    cycle: int = i % (self.selSize - 1)
                    p1: Genome = tGenomes[cycle]
                    p2: Genome = tGenomes[cycle + 1]
                    pop[i] = GenomeUtils.cross(p1, p2, self.cOpt)

        # save best performing genome after training process
        # get best performing genome
        GenomeUtils.save(tGenomes[0], runPref, self.genCap)
        GenomeUtils.saveInnov(innovMap, runPref, gen)


if __name__ == "__main__":
    for _ in range(50):
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
                    "pelletProgress": -5,
                    "lowestDistance": -3,
                    "won": -100,
                    "loss": 100,
                },
                "generationCap": 10000,
                "genomeConfig": {
                    "inSize": 9,
                    "outSize": 4,
                },
                "mutationConfig": {
                    "addNode": 0.2,
                    "addConn": 0.6,
                    "mutBias": 0.7,
                    "mutWeight": 0.7,
                    "mutConn": 0.5,
                },
                "populationSize": 50,
                "selectionSize": 10,
            },
            False,
        )
        training.start()
