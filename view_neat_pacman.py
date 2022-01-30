from tkinter import Tk
import _thread

from ai.neat.utils import GenomeUtils
from game.paiv import PAIV
from gui.controller import TimeController
from gui.display import Display


class App:
    def __init__(self, filename) -> None:
        self.game: PAIV = PAIV(GenomeUtils.load(filename), False, False)

        self.main: Tk = Tk()
        self.main.title("NEAT Performance View")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        self.timeController: TimeController = TimeController(0.1, self.nextStep)

        _thread.start_new_thread(self.timeController.start, ())

    def nextStep(self):
        gameover, won, atePellet = self.game.nextStep()

        if gameover or won or self.game.pelletDrought > 50:
            self.timeController.end()
            self.main.destroy()

        self.display.rerender(atePellet)

    def run(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":
    app = App("ne-gen150-30_01_2022_02_28_11.json")
    app.run()
