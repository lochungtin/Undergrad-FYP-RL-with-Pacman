from calendar import c
from tkinter import Canvas, Tk
from typing import List
from data.color import COLOR
from data.data import DIM, REP
from game.game import Game
from gui.utils import GUIUtil
from utils.coordinate import CPair


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

        self.canvas.delete("all")
        self.bindObjects()

    def createCanvasObject(self, x0: int, y0: int, x1: int, y1: int, xPad: int, yPad: int, rep: int) -> int:
        return self.canvas.create_rectangle(
            x0 + xPad, y0 + yPad, x1 - xPad, y1 - yPad, fill=self.color[rep], outline=""
        )

    def bindObjects(self) -> None:
        for rowIndex, stateRow in enumerate(self.game.state):
            for colIndex, cellObj in enumerate(stateRow):
                cellId: str = cellObj.id
                cell: int = cellObj.val

                x0, y0, x1, y1 = GUIUtil.calculatePos(rowIndex, colIndex)

                if cell == REP.PELLET:
                    canvasItemId: int = self.createCanvasObject(x0, y0, x1, y1, DIM.PAD_PELLET, DIM.PAD_PELLET, cell)
                    self.game.pellets[cellId].setCanvasItemId(canvasItemId)

                elif cell == REP.PWRPLT:
                    canvasItemId: int = self.createCanvasObject(x0, y0, x1, y1, DIM.PAD_PWRPLT, DIM.PAD_PWRPLT, cell)
                    self.game.pwrplts[cellId].setCanvasItemId(canvasItemId)

                elif cell == REP.DOOR:
                    canvasItemId: int = self.createCanvasObject(x0, y0, x1, y1, 0, DIM.PAD_DOOR, cell)

                elif cell != REP.EMPTY:
                    canvasItemId: int = self.createCanvasObject(x0, y0, x1, y1, 0, 0, cell)

                    # add canvas item id to movable
                    if cell == REP.PACMAN:
                        self.game.pacman.setCanvasItemId(canvasItemId)
                    elif REP.isGhost(cell):
                        self.game.ghosts[cell].setCanvasItemId(canvasItemId)

    def rerender(self) -> None:
        # remove pellet
        if self.game.lastPelletId != -1:
            self.canvas.delete(self.game.lastPelletId)

        if self.game.lastPwrPltId != -1:
            self.canvas.delete(self.game.lastPwrPltId)

        pPos = self.game.pacman.pos
        # update pacman location
        if self.game.pacman.moved:
            pdX, pdY = GUIUtil.calculateDxDy(pPos, self.game.pacman.prevPos)
            self.canvas.move(self.game.pacman.canvasItemId, pdX, pdY)

        # ghost updates
        for ghost in self.game.ghostList:
            # update path display
            if hasattr(ghost, "pathId"):
                if ghost.pathId != -1:
                    self.canvas.delete(ghost.pathId)

                # update path display
                if not ghost.isFrightened:
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
