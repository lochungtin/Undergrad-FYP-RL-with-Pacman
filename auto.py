from tkinter import Tk
import _thread

from data.data import AGENT_CLASS_TYPE, REP
from game.game import Game, newGame
from gui.controller import TimeController
from gui.display import Display
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # create game
        self.game: Game = newGame(config["agents"], config["enablePwrPlt"], config["neuralnets"], config["genomes"])

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
        self.display.rerender()

        if gameover or won:
            printPacmanPerfomance(0, self.game)

            self.tc.end()
            self.main.destroy()

    # run gui
    def start(self) -> None:
        self.main.mainloop()


if __name__ == "__main__":

    app: App = App(
        {
            "agents": {
                REP.PACMAN: AGENT_CLASS_TYPE.SMDP,
                REP.BLINKY: AGENT_CLASS_TYPE.NEAT,
                "secondary": AGENT_CLASS_TYPE.RAND,
            },
            "enablePwrPlt": True,
            "gameSpeed": 0.025,
            "genomes": {
                REP.BLINKY: ("out", "NE2303_0111", 280),
            },
            "neuralnets": {
                # REP.PACMAN: ("saves", "pacman", 63),
                REP.BLINKY: ("out", "RL2103_1506", 10000),
            },
        }
    )
    app.start()
