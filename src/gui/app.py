from threading import *
from tkinter import *
import sys
import time

from data import DIM, DIR, REP
from game.game import Game


class GUI:
    def __init__(self) -> None:
        # create game object
        self.game = Game()

        # create application
        self.main = Tk()
        self.main.title("Pacman")

        # bind key hanlders
        self.main.bind("<Up>", lambda _: self.game.pacman.setDir(DIR.UP))
        self.main.bind("<Down>", lambda _: self.game.pacman.setDir(DIR.DW))
        self.main.bind("<Left>", lambda _: self.game.pacman.setDir(DIR.LF))
        self.main.bind("<Right>", lambda _: self.game.pacman.setDir(DIR.RT))
        self.main.bind("<space>", self.togglePause)

        # handle kill event
        self.main.protocol("WM_DELETE_WINDOW", self.kill)
        
        # create canvas object
        self.canvas = Canvas(
            self.main,
            width=DIM.GBL_W,
            height=DIM.GBL_H,
            background=REP.COLOR_MAP[REP.BG],
            highlightthickness=0,
        )
        self.canvas.pack()

        # initialise game
        self.initialGame()

        # start update loop
        self.playing = True
        self.running = True
        Thread(target=self.controller).start()

    # create canvas objects from displayable list
    def initialGame(self):
        pass

    # time controller
    def controller(self) -> None:
        while self.running:
            if self.playing:
                time.sleep(0.1)

                gameover = self.game.nextState()
                # reset game and grid after gameover
                if gameover:
                    self.canvas.delete('all')

                    self.game = Game()
                    self.initialGame()

                self.updateCanvas()

    # pause game
    def togglePause(self, event) -> None:
        self.playing = not self.playing

    # kill program
    def kill(self) -> None:
        self.running = False
        self.main.destroy()

    # run main loop of application
    def run(self) -> None:
        self.main.mainloop()
        sys.exit()
