from tkinter import Canvas, Tk
from typing import List
from data.color import COLOR
from data.data import DIM, REP
from game.game import Game
from gui.utils import GUIUtil


class Display:
    def __init__(self, main: Tk, color: dict[int, str] = COLOR.DARK_FLAT) -> None:
        # set color mapping
        self.color: dict[int, str] = color

        # create canvas and add to window
        self.canvas: Canvas = Canvas(
            main, width=DIM.GBL_W, height=DIM.GBL_H, background=self.color[REP.BG], highlightthickness=0
        )
        self.canvas.pack()

    def newGame(self, game: Game) -> None:
        self.game = game

        for row in self.game.state:
            for cell in row:
                print(cell)

        self.canvas.delete("all")
        self.bindObjects()

        print()

        for row in self.game.state:
            for cell in row:
                print(cell)


    # create canvas object and return canvas id
    def createCanvasObject(self, x0: int, y0: int, x1: int, y1: int, xPad: int, yPad: int, rep: int) -> int:
        return self.canvas.create_rectangle(
            x0 + xPad, y0 + yPad, x1 - xPad, y1 - yPad, fill=self.color[rep], outline=""
        )

    # bind game objects to display canvas
    def bindObjects(self) -> None:
        # create ghosts
        for ghost in self.game.ghostList:
            x0, y0, x1, y1 = GUIUtil.calculatePos(ghost.pos)
            ghost.canvasItemId = self.createCanvasObject(x0, y0, x1, y1, 0, 0, ghost.repId)

        # create pacman
        x0, y0, x1, y1 = GUIUtil.calculatePos(self.game.pacman.pos)
        self.game.pacman.canvasItemId = self.createCanvasObject(x0, y0, x1, y1, 0, 0, REP.PACMAN)

        # create fixtures and pellets
        for row in self.game.state:
            for cell in row:
                x0, y0, x1, y1 = GUIUtil.calculatePos(cell.coords)

                if cell.hasPellet:
                    canvasItemId: int = self.createCanvasObject(
                        x0, y0, x1, y1, DIM.PAD_PELLET, DIM.PAD_PELLET, REP.PELLET
                    )
                    self.game.pellets[cell.id].setCanvasItemId(canvasItemId)

                # elif cell.hasPwrplt:
                #     canvasItemId: int = self.createCanvasObject(
                #         x0, y0, x1, y1, DIM.PAD_PWRPLT, DIM.PAD_PWRPLT, REP.PELLET
                #     )
                #     self.game.pwrplts[cell.id].setCanvasItemId(canvasItemId)

                elif cell.iSDoor:
                    canvasItemId: int = self.createCanvasObject(x0, y0, x1, y1, 0, DIM.PAD_DOOR, REP.DOOR)

                elif cell.isWall:
                    canvasItemId: int = self.createCanvasObject(x0, y0, x1, y1, 0, 0, REP.WALL)

    # rerender movable and destroyable objects
    def rerender(self) -> None:
        # remove pellet
        if self.game.lastPelletId != -1:
            self.canvas.delete(self.game.lastPelletId)

        if self.game.lastPwrPltId != -1:
            self.canvas.delete(self.game.lastPwrPltId)

        # ghost updates
        for ghost in self.game.ghostList:
            # update path display
            if hasattr(ghost, "pathId"):
                if ghost.pathId != -1:
                    self.canvas.delete(ghost.pathId)

                # update path display
                if not ghost.isFrightened and not ghost.isDead:
                    displayPath: List[int] = []
                    for cpair in ghost.path:
                        x, y = GUIUtil.calculateMidPt(cpair)
                        displayPath.append(x)
                        displayPath.append(y)

                    if len(displayPath) > 2:
                        ghost.pathId = self.canvas.create_line(displayPath, width=3, fill=self.color[ghost.repId])

            # update color
            if ghost.isDead:
                self.canvas.itemconfig(ghost.canvasItemId, fill=self.color[REP.DEAD])
            elif ghost.isFrightened:
                self.canvas.itemconfig(ghost.canvasItemId, fill=self.color[REP.FRIGHTENED])
            else:
                self.canvas.itemconfig(ghost.canvasItemId, fill=self.color[ghost.repId])

            # update location
            if ghost.moved:
                dX, dY = GUIUtil.calculateDxDy(ghost.pos, ghost.prevPos)
                self.canvas.move(ghost.canvasItemId, dX, dY)

        pPos = self.game.pacman.pos
        # update pacman location
        if self.game.pacman.moved:
            pdX, pdY = GUIUtil.calculateDxDy(pPos, self.game.pacman.prevPos)
            self.canvas.move(self.game.pacman.canvasItemId, pdX, pdY)
