from typing import Tuple
from agents.base import GhostAgent
from agents.blinky import BlinkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from agents.pacman import PlayableAgent
from game.game import Game
from tkinter import Tk
import _thread

from data.data import DIR
from game.game import Game
from gui.controller import TimeController
from gui.display import Display


# app class
class App:
    def __init__(self, manualControl: bool, enableGhost: bool = True, enablePwrPlt: bool = True) -> None:
        # save game config
        self.enableGhost: bool = enableGhost
        self.enablePwrPlt: bool = enablePwrPlt

        # create game object
        self.game: Game = Game(
            PlayableAgent(),
            BlinkyClassicAgent(),
            InkyClassicAgent(),
            ClydeClassicAgent(),
            PinkyClassicAgent(),
            self.enableGhost,
            self.enablePwrPlt,
        )

        # create time controller object
        self.timeController: TimeController = TimeController(0.075, self.nextStep)

        # create application
        self.main: Tk = Tk()
        self.main.title("Pacman")

        # bind key hanlders
        self.main.bind("<Up>", lambda _: self.game.pacman.setDir(DIR.UP))
        self.main.bind("<Down>", lambda _: self.game.pacman.setDir(DIR.DW))
        self.main.bind("<Left>", lambda _: self.game.pacman.setDir(DIR.LF))
        self.main.bind("<Right>", lambda _: self.game.pacman.setDir(DIR.RT))

        # create game display and bind game objects
        self.display: Display = Display(self.main)
        self.display.newGame(self.game)

        # bind nextStep() controllers
        if manualControl:
            self.main.bind("<space>", lambda _: self.nextStep())
        else:
            _thread.start_new_thread(self.timeController.start, ())

    # trigger Game.nextStep() and update dislay, reset if gameover
    def nextStep(self):
        # update game, proceed to next step
        gameover, won, atePellet = self.game.nextStep()

        # handle gameover
        if gameover:
            # create new game
            self.game = Game(
                PlayableAgent(),
                BlinkyClassicAgent(),
                InkyClassicAgent(),
                ClydeClassicAgent(),
                PinkyClassicAgent(),
                self.enableGhost,
                self.enablePwrPlt,
            )
            self.display.newGame(self.game)

        # update display
        self.display.rerender(atePellet)

    # run main loop of application
    def run(self) -> None:
        self.main.mainloop()


# execute app
if __name__ == "__main__":
    app = App(manualControl=False, enableGhost=True, enablePwrPlt=True)
    app.run()
