import _thread
from tkinter import Tk
from typing import List


from agents.blinky import BlinkyClassicAgent
from agents.clyde import ClydeClassicAgent
from agents.inky import InkyClassicAgent
from agents.pinky import PinkyClassicAgent
from agents.pacman import PlayableAgent, pacmanFeatureExtraction
from utils.direction import DIR
from game.game import Game
from gui.controller import TimeController
from gui.display import Display


# app class
class App:
    def __init__(self, manualControl: bool) -> None:
        # create game object
        self.game: Game = self.newGame()

        # create time controller object
        self.timeController: TimeController = TimeController(0.1, self.nextStep)

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

    def newGame(self):
        return Game(
            PlayableAgent(),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent(),
        )

    # trigger Game.nextStep() and update dislay, reset if gameover
    def nextStep(self):
        # update game, proceed to next step
        gameover, won, atePellet, atePwrPlt, ateGhost = self.game.nextStep()
        

        # timestep based
        reward: int = -1

        # punish stationary action
        if not self.game.pacman.moved:
            reward = -10
        # reward eating pellet
        elif atePellet:
            reward = 10
        # reward eating power pellet
        elif atePwrPlt:
            reward = 3
        # reward a kill
        elif ateGhost:
            reward = 25

        print(reward)

        # handle gameover
        if gameover or won:
            print(self.game.timesteps)

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
    App(manualControl=True).run()
