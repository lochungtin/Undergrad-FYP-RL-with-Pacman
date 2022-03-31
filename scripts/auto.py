from tkinter import Tk
import _thread

from data.data import AGENT_CLASS_TYPE, REP
from game.game import Game, newGame
from gui.controller import TimeController
from gui.display import Display


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
            "gameSpeed": 0.05,
            "genomes": {
                REP.BLINKY: ("saves", "ghost", 33),
                REP.PINKY: ("saves", "ghost", 33),
            },
            "neuralnets": {
                REP.PACMAN: ("saves", "pacman", 63),
                REP.BLINKY: ("saves", "ghost", 35),
                REP.PINKY: ("saves", "ghost", 35),
            },
        }
    )
    app.start()
