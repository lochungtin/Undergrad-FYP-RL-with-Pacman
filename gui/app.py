from threading import Thread
from tkinter import *
import sys
import time
from typing import Tuple

from data import DIM, DIR, REP
from game.game import Game


class App:
    def __init__(self) -> None:
        # create game object
        self.game: Game = Game()

        # create application
        self.main: Tk = Tk()
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
        self.canvas: Canvas = Canvas(
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
        self.playing: bool = True
        self.running: bool = True
        # Thread(target=self.controller).start()

    # calculate pixel position of grid
    def calculatePos(self, row, col) -> Tuple[int, int, int, int]:
        x0: int = col * DIM.JUMP
        y0: int = row * DIM.JUMP
        return x0, y0, x0 + DIM.CELL, y0 + DIM.CELL

    # create canvas objects from displayable list
    def initialGame(self):
        # draw grid
        for rowIndex, stateRow in enumerate(self.game.state):
            for colIndex, cell in enumerate(stateRow):
                x0, y0, x1, y1 = self.calculatePos(rowIndex, colIndex)

                if REP.isPellet(cell):
                    # draw pellets
                    if cell == REP.PELLET:
                        canvasItemId: int = self.canvas.create_rectangle(
                            x0 + DIM.PAD_PELLET,
                            y0 + DIM.PAD_PELLET,
                            x1 - DIM.PAD_PELLET,
                            y1 - DIM.PAD_PELLET,
                            fill=REP.COLOR_MAP[cell],
                            outline="",
                        )
                    # draw power pellet
                    else:
                        canvasItemId: int = self.canvas.create_rectangle(
                            x0 + DIM.PAD_PWRPLT,
                            y0 + DIM.PAD_PWRPLT,
                            x1 - DIM.PAD_PWRPLT,
                            y1 - DIM.PAD_PWRPLT,
                            fill=REP.COLOR_MAP[cell],
                            outline="",
                        )

                    # add canvas item id to pellet object
                    self.game.pellets[rowIndex][colIndex].setCanvasItemId(canvasItemId)
                elif cell != REP.EMPTY:
                    canvasItemId: int = self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[cell], outline=""
                    )

                    # add canvas item id to movable
                    if cell == REP.PACMAN:
                        self.game.pacman.setCanvasItemId(canvasItemId)
                    elif cell == REP.BLINKY:
                        self.game.blinky.setCanvasItemId(canvasItemId)
                    elif cell == REP.INKY:
                        self.game.inky.setCanvasItemId(canvasItemId)
                    elif cell == REP.CLYDE:
                        self.game.clyde.setCanvasItemId(canvasItemId)
                    elif cell == REP.PINKY:
                        self.game.pinky.setCanvasItemId(canvasItemId)

    # time controller
    def controller(self) -> None:
        while self.running:
            if self.playing:
                time.sleep(0.1)

                # reset game and grid after gameover
                if self.game.nextStep():
                    self.canvas.delete("all")

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
