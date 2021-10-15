from threading import *
from tkinter import *
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
        self.main.bind("<Up>", lambda _: self.handleKey(DIR.UP))
        self.main.bind("<Down>", lambda _: self.handleKey(DIR.DW))
        self.main.bind("<Left>", lambda _: self.handleKey(DIR.LF))
        self.main.bind("<Right>", lambda _: self.handleKey(DIR.RT))
        self.main.bind("<space>", lambda _: self.game.togglePause())
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

                x0, y0, x1, y1 = self.calPxPos(row, col)

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

        # draw pacman
        pacmanRow, pacmanCol = POS.PACMAN
        self.game.pacman.setDiplayObj(
            self.canvas.create_rectangle(
                self.calPxPos(pacmanRow, pacmanCol),
                fill=REP.COLOR_MAP[REP.PACMAN],
                outline="",
            )
        )
        self.game.setState(pacmanRow, pacmanCol, REP.PACMAN)

        # start update loop
        self.running = True
        Thread(target=self.tCtrl).start()

    # calculate pixel positions
    def calPxPos(self, row, col):
        positioner = DIM.CELL + DIM.GAP

        x0 = col * positioner
        y0 = row * positioner

        return x0, y0, x0 + DIM.CELL, y0 + DIM.CELL

    # keystroke handlers
    def handleKey(self, keyID):
        self.game.pacman.setDir(keyID)

        print("pressed: {}".format(keyID))

    # update canvas
    def updateCanvas(self):
        dx, dy = self.game.pacman.getDisplayDelta()
        self.canvas.move(self.game.pacman.diplay, dx, dy)
        return

    # time controller
    def tCtrl(self):
        while self.running:
            time.sleep(0.1)

            self.game.nextState()
            self.updateCanvas()

    def kill(self):
        self.running = False
        self.main.destroy()

    # start app
    def run(self):
        # run main loop of application
        self.main.mainloop()
