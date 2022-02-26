from time import time
from tkinter import Canvas
from typing import List, Tuple

from agents.base import DirectionAgent, GhostAgent
from agents.pacman import pacmanFeatureExtraction
from data.config import BOARD, POS
from data.data import GHOST_MODE, REP
from game.components.pellet import Pellet, PowerPellet
from game.utils.pathfinder import PathFinder
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR
from utils.grid import createGameSizeGrid


class Game:
    def __init__(
        self,
        pacman: DirectionAgent,
        blinky: GhostAgent = None,
        inky: GhostAgent = None,
        clyde: GhostAgent = None,
        pinky: GhostAgent = None,
        enablePwrPlt: bool = True,
    ) -> None:
        # game timesteps
        self.timesteps: int = 0

        # power pellet availablility
        self.enablePwrPlt: bool = enablePwrPlt

        # pellets
        self.pellets: dict[str, Pellet] = {}
        self.pelletProgress: int = BOARD.TOTAL_PELLET_COUNT

        self.pwrplts: dict[str, PowerPellet] = {}
        self.pwrpltEffectCounter: int = 0

        # create pellets and fill game state
        self.state: List[List[Cell]] = createGameSizeGrid(None)

        for i, row in enumerate(BOARD.DATA):
            r: List[Cell] = []
            for j, val in enumerate(row):
                cell = Cell(i, j, val)

                self.state[i][j] = cell

                if val == REP.PELLET:
                    self.pellets[cell.id] = Pellet(cell.coords)
                elif val == REP.PWRPLT:
                    if enablePwrPlt:
                        self.pwrplts[cell.id] = PowerPellet(cell.coords)
                    else:
                        cell.hasPwrplt = False

        # game agents
        self.pacman: DirectionAgent = pacman
        self.getCell(self.pacman.pos).hasPacman = True

        self.ghosts: dict[str, GhostAgent] = {REP.BLINKY: blinky, REP.INKY: inky, REP.CLYDE: clyde, REP.PINKY: pinky}
        self.ghostList: List[GhostAgent] = []
        for key, ghost in self.ghosts.items():
            if not ghost is None:
                self.ghostList.append(ghost)

                gCell: Cell = self.getCell(ghost.pos)
                gCell.hasGhost = True
                gCell.ghosts[ghost.repId] = True

        self.ghostModeIndex: int = 0
        self.ghostMode: int = GHOST_MODE.GHOST_MODE_SCHEDULE[self.ghostModeIndex][0]
        self.ghostModeCounter: int = GHOST_MODE.GHOST_MODE_SCHEDULE[self.ghostModeIndex][1]

        # state cell connections
        # loop connection
        self.getCell(POS.LOOP_POS[0]).setAdj(DIR.LF, self.getCell(POS.LOOP_POS[1]))
        self.getCell(POS.LOOP_POS[1]).setAdj(DIR.RT, self.getCell(POS.LOOP_POS[0]))

        # normal cell connection
        for row in self.state:
            for cell in row:
                if cell.isWall:
                    continue

                for dirVal in DIR.getList():
                    newPos: CPair = cell.coords.move(dirVal)
                    if BOARD.isValidPos(newPos) and BOARD.DATA[newPos.row][newPos.col] != REP.WALL:
                        cell.setAdj(dirVal, self.state[newPos.row][newPos.col])

        # pathfinder
        self.pf: PathFinder = PathFinder(self.state)

        for ghost in self.ghostList:
            if ghost.isClassic:
                ghost.bindPathFinder(self.pf)

        # canvas object
        self.canvas: Canvas = None

        self.lastPelletId: int = -1
        self.lastPwrPltId: int = -1

    # bind cavnvas object to game
    def setCanvas(self, canvas: Canvas) -> None:
        self.canvas = canvas

    # retrieve vertex from grid
    def getCell(self, pos: CPair) -> Cell:
        return self.state[pos.row][pos.col]

    # handle eating of pellets
    def eatPellet(self, pos: CPair) -> int:
        posStr: str = pos.__str__()
        if posStr in self.pellets:
            pellet: Pellet = self.pellets[posStr]

            if pellet.valid:
                self.getCell(pos).hasPellet = False
                self.pelletProgress -= 1

                return pellet.destroy()

        return -1

    def eatPwrPlt(self, pos: CPair) -> int:
        posStr: str = pos.__str__()
        if posStr in self.pwrplts:
            pellet: Pellet = self.pwrplts[posStr]

            if pellet.valid:
                self.getCell(pos).hasPwrplt = False
                self.pwrpltEffectCounter = GHOST_MODE.GHOST_FRIGHTENED_STEP_COUNT

                return pellet.destroy()

        return -1

    # handle agent movement
    def movePacman(self, pos: CPair, pPos: CPair) -> None:
        self.getCell(pos).hasPacman = True
        self.getCell(pPos).hasPacman = False

    def moveGhost(self, ghostId: int, pos: CPair, pPos: CPair) -> None:
        cell: Cell = self.getCell(pos)
        cell.hasGhost = True
        cell.ghosts[ghostId] = True

        if pos != pPos:
            pCell: Cell = self.getCell(pPos)
            pCell.hasGhost = False
            pCell.ghosts[ghostId] = False

    # detect pacman and ghost collision
    def detectCollision(self, pPos: CPair, pPrevPos: CPair, gPos: CPair, gPrevPos: CPair) -> bool:
        return pPos == gPos or (pPrevPos == gPos and pPos == gPrevPos)

    # proceed to next time step
    def nextStep(self) -> Tuple[bool, bool, bool, bool, bool]:
        # timestep management
        self.timesteps += 1

        if self.pwrpltEffectCounter > -1:
            self.pwrpltEffectCounter -= 1

            if self.pwrpltEffectCounter == 0:
                for ghost in self.ghostList:
                    ghost.isFrightened = False

        newGhostMode: bool = False
        if self.ghostModeCounter > -1:
            self.ghostModeCounter -= 1

            if self.ghostModeCounter == 0:
                self.ghostModeIndex += 1

                self.ghostMode: int = GHOST_MODE.GHOST_MODE_SCHEDULE[self.ghostModeIndex][0]
                self.ghostModeCounter: int = GHOST_MODE.GHOST_MODE_SCHEDULE[self.ghostModeIndex][1]

                newGhostMode = True

        # reset pellet id
        self.lastPelletId = -1
        self.lastPwrPltId = -1

        # update pacman location
        pPos, pPrevPos, pMoved = self.pacman.getNextPos(self)
        if pMoved:
            self.movePacman(pPos, pPrevPos)

            self.lastPelletId: int = self.eatPellet(pPos)
            if self.pelletProgress < BOARD.CRUISE_ELROY_TRIGGER and not self.ghosts[REP.BLINKY] is None:
                self.ghosts[REP.BLINKY].cruiseElroy = True

            if self.canvas != None:
                self.canvas.delete(self.lastPelletId)

            if self.enablePwrPlt:
                self.lastPwrPltId: int = self.eatPwrPlt(pPos)

                if self.lastPwrPltId != -1:
                    for ghost in self.ghostList:
                        ghost.isFrightened = True

                if self.canvas != None:
                    self.canvas.delete(self.lastPwrPltId)

        # update ghost location
        ateGhost: bool = False
        for ghost in self.ghostList:
            if newGhostMode:
                if ghost.isClassic:
                    ghost.mode = self.ghostMode

            gPos, gPrevPos, gMoved = ghost.getNextPos(self)
            if gMoved:
                self.moveGhost(ghost.repId, gPos, gPrevPos)

            # handle collision
            if self.detectCollision(pPos, pPrevPos, gPos, gPrevPos):
                if not ghost.isDead:
                    if ghost.isFrightened:
                        ghost.isDead = True
                        ghost.isFrightened = False
                        ateGhost = True
                    else:
                        return (
                            True,
                            self.pelletProgress == 0,
                            self.lastPelletId == -1,
                            self.lastPwrPltId == -1,
                            ateGhost,
                        )

        return False, self.pelletProgress == 0, self.lastPelletId != -1, self.lastPwrPltId != -1, ateGhost
