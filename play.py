from tkinter import Tk
import _thread

from data.color import COLOR
from data.data import AGENT_CLASS_TYPE, REP
from utils.direction import DIR
from game.game import Game, newGame
from gui.controller import TimeController
from gui.display import Display


# app class
class App:
    def __init__(self, config: dict[str, object], manualControl: bool = False, retroColors: bool = False) -> None:
        # agent config
        self.agents: dict[str, object] = config["agents"]

        # game config
        self.enablePwrPlt: bool = config["enablePwrPlt"]

        # neural net
        self.neuralnets: dict[str, str] = config["neuralnets"]

        # genomes
        self.genomes: dict[str, str] = config["genomes"]

        # create game object
        self.game: Game = self.newGame()

        # create time controller object
        self.timeController: TimeController = TimeController(config["gameSpeed"], self.nextStep)

        # create application
        self.main: Tk = Tk()
        self.main.title("Pacman")

        # bind key hanlders
        self.main.bind("<Up>", lambda _: self.game.pacman.setDir(DIR.UP))
        self.main.bind("<Down>", lambda _: self.game.pacman.setDir(DIR.DW))
        self.main.bind("<Left>", lambda _: self.game.pacman.setDir(DIR.LF))
        self.main.bind("<Right>", lambda _: self.game.pacman.setDir(DIR.RT))

        # create game display and bind game objects
        self.display: Display = None
        if retroColors:
            self.display: Display = Display(self.main, COLOR.CLASSIC_RETRO)
        else:
            self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        # bind nextStep() controllers
        if manualControl:
            self.main.bind("<space>", lambda _: self.nextStep())
        else:
            _thread.start_new_thread(self.timeController.start, ())

    # create new game
    def newGame(self):
        return newGame(self.agents, self.enablePwrPlt, self.neuralnets, self.genomes)

    # trigger Game.nextStep() and update dislay, reset if gameover
    def nextStep(self):
        # update game, proceed to next step
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()

        # handle gameover
        if gameover or won:
            # create new game
            self.game = self.newGame()
            self.display.newGame(self.game)

        # update display
        self.display.rerender()

    # run main loop of application
    def run(self) -> None:
        self.main.mainloop()


# execute app
if __name__ == "__main__":
    app: App = App(
        {
            "agents": {
                REP.PACMAN: AGENT_CLASS_TYPE.CTRL,
                REP.BLINKY: AGENT_CLASS_TYPE.NEAT,
                "secondary": {
                    REP.INKY: AGENT_CLASS_TYPE.NONE,
                    REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                    REP.PINKY: AGENT_CLASS_TYPE.OGNL,
                },
            },
            "enablePwrPlt": True,
            "gameSpeed": 0.1,
            "genomes": {
                REP.BLINKY: ("out", "NE2303_0111", 380),
            },
            "neuralnets": {
                REP.BLINKY: ("out", "RL2103_1506", 10000),
            },
        },
        manualControl=True,
        retroColors=False,
    )
    app.run()
