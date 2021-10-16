from threading import *
from tkinter import *
import sys
import time

from .data.constants import *
from .game.game import Game


class GUI:
    def __init__(self):
        # create game object
        self.game = Game()

        # create application
        self.main = Tk()
        self.main.title('Pacman')
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
        Thread(target=self.timeController).start()

    # create canvas objects from displayable list
    def initialGame(self):
        # draw grid
        for row in range(BOARD.row):
            for col in range(BOARD.col):
                rep = self.game.state[row][col]

                x0, y0, x1, y1 = self.calPxPos((row, col))

                if rep == REP.WALL:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[rep], outline=""
                    )
                elif rep == REP.DOOR:
                    self.canvas.create_rectangle(
                        x0,
                        y0 + DIM.PAD_DOOR,
                        x1,
                        y1 - DIM.PAD_DOOR,
                        fill=REP.COLOR_MAP[rep],
                        outline="",
                    )

        # draw displayables and update state
        for movable in self.game.movables:
            self.game.setState(movable.pos, movable.rep)
            movable.setDiplayObj(
                self.canvas.create_rectangle(
                    self.calPxPos(movable.pos),
                    fill=REP.COLOR_MAP[movable.rep],
                    outline="",
                )
            )

        # draw pellets
        for row in self.game.pelletState:
            for pellet in row:
                if pellet == None:
                    continue

                x0, y0, x1, y1 = self.calPxPos(pellet.pos)

                padding = DIM.PAD_PELLET
                if pellet.rep == REP.PWRPLT:
                    padding = DIM.PAD_PWRPLT

                pellet.setDiplayObj(
                    self.canvas.create_rectangle(
                        x0 + padding,
                        y0 + padding,
                        x1 - padding,
                        y1 - padding,
                        fill=REP.COLOR_MAP[pellet.rep],
                        outline="",
                    )
                )

    # calculate pixel positions
    def calPxPos(self, pos):
        x0 = pos[1] * DIM.JUMP
        y0 = pos[0] * DIM.JUMP
        return x0, y0, x0 + DIM.CELL, y0 + DIM.CELL

    # update canvas
    def updateCanvas(self):
        # update positions of movables
        for movable in self.game.movables:
            dx, dy = movable.getDisplayDelta()
            self.canvas.move(movable.display, dx, dy)

            # destroy pellet object if cell is visited
            if movable.rep == REP.PACMAN:
                row, col = movable.pos

                cellObj = self.game.pelletState[row][col]
                if cellObj != None and not cellObj.valid:
                    self.canvas.delete(cellObj.display)

    # time controller
    def timeController(self):
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
