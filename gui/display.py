from tkinter import Canvas, Tk
from typing import List
from data.data import DIM, REP
from game.game import Game
from gui.utils import GUIUtil


class Display:
    def __init__(self, game: Game, main: Tk) -> None:
        self.game: Game = game

        # create canvas and add to window
        self.canvas: Canvas = Canvas(
            main,
            width=DIM.GBL_W,
            height=DIM.GBL_H,
            background=REP.COLOR_MAP[REP.BG],
            highlightthickness=0,
        )
        self.canvas.pack()

        self.bindObjects()

    def newGame(self, game: Game) -> None:
        self.game = game

        self.canvas.delete("all")
        self.bindObjects()

    def bindObjects(self) -> None:
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
                    if cell == REP.DOOR:
                        canvasItemId: int = self.canvas.create_rectangle(
                            x0,
                            y0 + DIM.PAD_DOOR,
                            x1,
                            y1 - DIM.PAD_DOOR,
                            fill=REP.COLOR_MAP[cell],
                            outline="",
                        )
                    else:
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

    def rerender(self, atePellet: bool) -> None:
        # remove pellet
        pPos = self.game.pacman.pos
        if atePellet:
            self.canvas.delete(self.game.pellets[pPos.row][pPos.col].canvasItemId)

        # update pacman location
        if self.game.pacman.moved:
            pdX, pdY = GUIUtil.calculateDxDy(pPos, self.game.pacman.prevPos)
            self.canvas.move(self.game.pacman.canvasItemId, pdX, pdY)

        # ghost updates
        if self.game.enableGhost:
            for ghost in self.game.ghosts:
                # delete old paths
                if hasattr(ghost.prevPath, "canvasItemId"):
                    self.canvas.delete(ghost.prevPath.canvasItemId)

                # update path display
                if not ghost.isFrightened:
                    displayPath: List[int] = []
                    for cpair in ghost.path.path:
                        x, y = GUIUtil.calculateMidPt(cpair)
                        displayPath.append(x)
                        displayPath.append(y)

                    if len(displayPath) > 2:
                        ghost.path.setCanvasItemId(
                            self.canvas.create_line(
                                displayPath, width=3, fill=REP.COLOR_MAP[ghost.repId]
                            )
                        )

                    # update color
                    if ghost.isDead:
                        self.canvas.itemconfig(
                            ghost.canvasItemId, fill=REP.COLOR_MAP[REP.DEAD]
                        )
                    else:
                        self.canvas.itemconfig(
                            ghost.canvasItemId, fill=REP.COLOR_MAP[ghost.repId]
                        )
                else:
                    self.canvas.itemconfig(
                        ghost.canvasItemId, fill=REP.COLOR_MAP[REP.FRIGHTENED]
                    )

                # update location
                if ghost.moved:
                    dX, dY = GUIUtil.calculateDxDy(ghost.pos, ghost.prevPos)
                    self.canvas.move(ghost.canvasItemId, dX, dY)
