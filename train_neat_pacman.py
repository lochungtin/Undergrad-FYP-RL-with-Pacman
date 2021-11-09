from tkinter import Tk
from typing import Tuple
import _thread
import time

from ai.neat.genome import Genome
from ai.neat.utils import Utils
from game.game import Game
from game.paiv import PAIV
from gui.display import Display


class NEATTraining:
    def __init__(self, hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("Pacman Training")

            self.display: Display = Display(self.main)

        # fitness coefficent
        self.cT: float = 0
        self.cP: float = 0
        self.cW: float = 0
        self.cL: float = 0

    def runSim(
        self, genome: Genome, enableGhost: bool, enablePwrPlt: bool
    ) -> Tuple[float, int, int, bool, bool]:
        game: PAIV = PAIV(genome, enableGhost, enablePwrPlt)

        if self.hasDisplay:
            self.display.newGame(game)
            self.display.bindObjects()

        pelletCount: int = 0
        gameover: bool = False
        won: bool = False
        while game.pelletDrought < 100 and not gameover and not won:
            gameover, won, atePellet = game.nextStep()

            if self.hasDisplay:
                self.display.rerender(atePellet)

                time.sleep(0.05)


            if atePellet:
                pelletCount += 0

        genome.fitness = (
            self.cT * game.timesteps
            + self.cP * pelletCount
            + self.cW * won
            + self.cL * gameover
        )

        return genome.fitness, game.timesteps, pelletCount, gameover, won

    def startTrainingLoop(self) -> None:
        t: int = 0
        while t < 10:
            g = Genome(10, 4)
            g.baseInit() 
            print(self.runSim(g, enableGhost=False, enablePwrPlt=False))


    def start(self) -> None:
        _thread.start_new_thread(self.startTrainingLoop, ())

        # start display
        if self.hasDisplay:
            self.main.mainloop()


if __name__ == "__main__":
    training: NEATTraining = NEATTraining(True)
    training.start()
