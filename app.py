from threading import *
from tkinter import *
import sys
import time

from constants import *
from game import Game


class App:
    def __init__(self):
        # initialise game object
        self.game = Game()

        # create application object
        self.main = Tk()
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
            background="#1E1E1E",
            highlightthickness=0,
        )
        self.canvas.pack()

        # draw grid
        for row in range(BOARD.row):
            for col in range(BOARD.col):
                rep = self.game.state[row][col]

                x0, y0, x1, y1 = self.calPxPos((row, col))

                if rep == 2:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[REP.EMPTY], outline=""
                    )
                    self.canvas.create_rectangle(
                        x0,
                        y0 + DIM.PAD_DOOR,
                        x1,
                        y1 - DIM.PAD_DOOR,
                        fill=REP.COLOR_MAP[rep],
                        outline="",
                    )
                else:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[rep], outline=""
                    )

        # draw movables
        self.game.pacman.setDiplayObj(
            self.canvas.create_rectangle(
                self.calPxPos(POS.PACMAN), fill=REP.COLOR_MAP[REP.PACMAN], outline=""
            )
        )

        self.game.blinky.setDiplayObj(
            self.canvas.create_rectangle(
                self.calPxPos(POS.BLINKY), fill=REP.COLOR_MAP[REP.BLINKY], outline=""
            )
        )

        self.game.inky.setDiplayObj(
            self.canvas.create_rectangle(
                self.calPxPos(POS.INKY), fill=REP.COLOR_MAP[REP.INKY], outline=""
            )
        )

        self.game.clyde.setDiplayObj(
            self.canvas.create_rectangle(
                self.calPxPos(POS.CLYDE), fill=REP.COLOR_MAP[REP.CLYDE], outline=""
            )
        )

        self.game.pinky.setDiplayObj(
            self.canvas.create_rectangle(
                self.calPxPos(POS.PINKY), fill=REP.COLOR_MAP[REP.PINKY], outline=""
            )
        )

        # update state
        self.game.setState(POS.PACMAN, REP.PACMAN)
        self.game.setState(POS.BLINKY, REP.BLINKY)
        self.game.setState(POS.INKY, REP.INKY)
        self.game.setState(POS.CLYDE, REP.CLYDE)
        self.game.setState(POS.PINKY, REP.PINKY)

        # start update loop
        self.playing = True
        self.running = True
        t = Thread(target=self.tCtrl)
        t.start()

    # calculate pixel positions
    def calPxPos(self, pos):
        x0 = pos[1] * DIM.JUMP
        y0 = pos[0] * DIM.JUMP
        return x0, y0, x0 + DIM.CELL, y0 + DIM.CELL

    # update canvas
    def updateCanvas(self):
        # update pacman position
        pacmanDX, pacmanDY = self.game.pacman.getDisplayDelta()
        self.canvas.move(self.game.pacman.diplay, pacmanDX, pacmanDY)

    # time controller
    def tCtrl(self):
        while self.running:
            if self.playing:
                time.sleep(0.1)

                try:
                    self.game.nextState()
                    self.updateCanvas()
                except:
                    sys.exit()

    # pause program
    def togglePause(self, event):
        self.playing = not self.playing

    # kill program
    def kill(self):
        self.running = False
        self.main.destroy()

    # start app
    def run(self):
        # run main loop of application
        self.main.mainloop()
        sys.exit()
