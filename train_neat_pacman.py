from tkinter import Tk
from typing import List, Tuple
import _thread
import time

from ai.neat.genome import Genome
from ai.neat.utils import Utils
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
        self.populationSize: int = trainingConfig["populationSize"]
        self.genomeInSize: int = trainingConfig["genomeConfig"]["inSize"]
        self.genomeOutSize: int = trainingConfig["genomeConfig"]["outSize"]

        # distance compatibility config
        self.compDistThres: float = trainingConfig["compDistThres"]
        self.cExcess: float = trainingConfig["compDistCoeff"]["excess"]
        self.cDisjoint: float = trainingConfig["compDistCoeff"]["disjoint"]
        self.cWeight: float = trainingConfig["compDistCoeff"]["weight"]

        # fitness coefficent
        self.cTimestep: float = trainingConfig["fitnessCoeff"]["timesteps"]
        self.cPellet: float = trainingConfig["fitnessCoeff"]["pellets"]
        self.cWin: float = trainingConfig["fitnessCoeff"]["win"]
        self.cLoss: float = trainingConfig["fitnessCoeff"]["loss"]

        # population
        self.population: List[Genome] = []
        # create initial population
        for _ in range(self.populationSize):
            genome = Genome(self.genomeInSize, self.genomeOutSize)
            genome.baseInit()
            self.population.append(genome)

        # generation data
        self.generationCap: int = trainingConfig["generationCap"]
        self.generation: int = 0

    def runSim(self, genome: Genome) -> Tuple[float, int, int, bool, bool]:
        game: PAIV = PAIV(genome, self.enableGhost, self.enablePwrPlt)

        if self.hasDisplay:
            self.display.newGame(game)

        pelletCount: int = 0
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

        genome.fitness = (
            self.cTimestep * game.timesteps
            + self.cPellet * pelletCount
            + self.cWin * won
            + self.cLoss * (gameover or game.pelletDrought >= 50)
        )

        return genome.fitness, game.timesteps, pelletCount, gameover, won

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
        # initial mutations

        while self.generation < self.generationCap:
            self.generation += 1

            # run simulation
            for genome in self.population:
                self.runSim(genome)

                # adjust fitness values
                Utils.adjFitness(
                    genome,
                    self.population,
                    self.cExcess,
                    self.cDisjoint,
                    self.cWeight,
                    self.compDistThres,
                )

            # segregation
            reps: List[Genome] = []
            species: List[List[Genome]] = []
            for genome in self.population:
                if len(reps) == 0:
                    reps.append(genome)
                    species.append([genome])
                else:
                    assigned = False
                    for index, r in enumerate(reps):
                        if (
                            Utils.getCompDist(
                                genome, r, self.cExcess, self.cDisjoint, self.cWeight
                            )
                            < self.compDistThres
                        ):
                            species[index].append(genome)
                            assigned = True
                            break

                    if not assigned:
                        reps.append(genome)
                        species.append([genome])

            # select fittest and reproduce
            for genomes in species:
                genomes.sort(key=lambda g: g.fitness, reverse=True)
                pass

            # mutate offsprings


if __name__ == "__main__":
    training: NEATTraining = NEATTraining(
        {
            "compDistCoeff": {
                "disjoint": 1,
                "excess": 1,
                "weight": 1,
            },
            "compDistThres": 0.75,
            "fitnessCoeff": {
                "timesteps": -1,
                "pellets": 10,
                "win": 1000,
                "loss": -1000,
            },
            "generationCap": 1,
            "genomeConfig": {
                "inSize": 10,
                "outSize": 4,
            },
            "populationSize": 100,
            "simulationConfig": {
                "ghost": False,
                "pwrplt": False,
            },
        },
        False,
    )
    training.start()
