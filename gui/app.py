from tkinter import *

from data import DIM, DIR, REP
from game.game import Game
from gui.util import GUIUtil


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
        self.main.bind("<space>", lambda _: self.nextStep())

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

        # bind objects with canvas items
        self.initialGame()

    # create canvas objects from displayable list
    def initialGame(self) -> None:
        # draw grid
        for rowIndex, stateRow in enumerate(self.game.state):
            for colIndex, cell in enumerate(stateRow):
                x0, y0, x1, y1 = GUIUtil.calculatePos(rowIndex, colIndex)

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

    # trigger Game.nextStep() and update canvas
    # reset canvas if gameover
    def nextStep(self):
        print('a')
        gameover, won = self.game.nextStep()

        # update pacman's location
        if self.game.pacman.moved:
            pdX, pdY = GUIUtil.calculateDxDy(self.game.pacman.pos, self.game.pacman.prevPos)
            self.canvas.move(self.game.pacman.canvasItemId, pdX, pdY)

        # update ghosts' locations
        for ghost in self.game.ghosts:
            dX, dY = GUIUtil.calculateDxDy(ghost.pos, ghost.prevPos)
            self.canvas.move(ghost.canvasItemId, dX, dY)

        if gameover:
            # clear canvas
            self.canvas.delete("all")

            # create new game and bind objects with canvas items
            self.game = Game()
            self.initialGame()

    # kill program
    def kill(self) -> None:
        self.main.destroy()

    # run main loop of application
    def run(self) -> None:
        self.main.mainloop()
