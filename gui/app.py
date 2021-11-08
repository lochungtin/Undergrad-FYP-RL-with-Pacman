from tkinter import Canvas, Tk
from typing import List
import _thread

from data import DIM, DIR, REP
from game.game import Game
from gui.controller import TimeController
from gui.utils import GUIUtil


class App:
    def __init__(
        self,
        manualControl: bool,
        enableGhost: bool = True,
        enablePwrPlt: bool = True,
    ) -> None:
        # create game object
        self.game: Game = Game(enableGhost, enablePwrPlt)
        # save game config
        self.enableGhost: bool = enableGhost
        self.enablePwrPlt: bool = enablePwrPlt

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
        self.initialiseGame()

        # bind nextStep() controllers
        if manualControl:
            self.main.bind("<space>", lambda _: self.nextStep())
        else:
            _thread.start_new_thread(self.timeController.start, ())

    # create canvas objects from displayable list
    def initialiseGame(self) -> None:
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

    # trigger Game.nextStep() and update canvas
    # reset canvas if gameover
    def nextStep(self):
        if self.enableGhost:
            for ghost in self.game.ghosts:
                # delete old paths
                if hasattr(ghost.path, "canvasItemId"):
                    self.canvas.delete(ghost.path.canvasItemId)

        # update game, proceed to next step
        gameover, won, atePellet = self.game.nextStep()

        # remove pellet
        pPos = self.game.pacman.pos
        if atePellet:
            self.canvas.delete(self.game.pellets[pPos.row][pPos.col].canvasItemId)

        # update pacman location
        if self.game.pacman.moved:
            pdX, pdY = GUIUtil.calculateDxDy(pPos, self.game.pacman.prevPos)
            self.canvas.move(self.game.pacman.canvasItemId, pdX, pdY)

        # ghost updates
        if self.enableGhost:
            for ghost in self.game.ghosts:
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

        if gameover:
            # clear canvas
            self.canvas.delete("all")

            # create new game and bind objects with canvas items
            self.game = Game(self.enableGhost, self.enablePwrPlt)
            self.initialiseGame()

    # kill program
    def kill(self) -> None:
        self.main.destroy()

    # run main loop of application
    def run(self) -> None:
        self.main.mainloop()
