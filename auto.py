from tkinter import Tk
import _thread

from data.data import GHOST_CLASS_TYPE
from game.game import Game
from gui.controller import TimeController
from gui.display import Display
from utils.game import newGame
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # create game
        self.game: Game = newGame(
            config["ghosts"],
            config["enablePwrPlt"],
            config["neuralnets"],
            config["genomes"],
        )

        # creat gui
        self.main: Tk = Tk()
        self.main.title("Auto Pacman Game Viewer")

        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        # create and enable auto timestep controller
        self.tc: TimeController = TimeController(config["gameSpeed"], self.nextStep)

        _thread.start_new_thread(self.tc.start, ())

    # perform update step
    def nextStep(self):
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()

        if gameover or won:
            printPacmanPerfomance(0, self.game)

            self.tc.end()
            self.main.destroy()

        self.display.rerender()

    # run gui
    def start(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":
    app: App = App(
        {
            "enablePwrPlt": True,
            "gameSpeed": 0.05,
            "genomes": {},
            "ghosts": {
                "blinky": GHOST_CLASS_TYPE.OGNL,
                "inky": GHOST_CLASS_TYPE.NONE,
                "clyde": GHOST_CLASS_TYPE.NONE,
                "pinky": GHOST_CLASS_TYPE.OGNL,
            },
            "iterations": 30,
            "neuralnets": {
                "pacman": ("saves", "pacman", 70),
                "blinky": ("out", "RL0803_1642", 500),
            },
        }
    )
    app.start()
