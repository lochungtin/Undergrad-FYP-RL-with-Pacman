from copy import deepcopy
from pathlib import Path
from tkinter import Canvas
from typing import List, Tuple

from agents.base import DirectionAgent, GhostAgent
from data.config import BOARD, POS
from data.data import DATA, REP
from game.components.pellet import Pellet, PowerPellet
from game.utils.pathfinder import PathFinder
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR


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
        self.pelletProgress: int = DATA.TOTAL_PELLET_COUNT

        self.pwrplts: dict[str, PowerPellet] = {}
        self.pwrpltEffectCounter: int = 0

        # create pellets and fill game state
        self.state: List[List[Cell]] = []

        for i, row in enumerate(BOARD.DATA):
            r: List[Cell] = []
            for j, val in enumerate(row):
                cell = Cell(i, j, val)
                r.append(cell)

                if val == REP.PELLET:
                    self.pellets[cell.id] = Pellet(cell.coords)
                elif val == REP.PWRPLT and enablePwrPlt:
                    self.pwrplts[cell.id] = PowerPellet(cell.coords)

            self.state.append(r)

        # game agents
        self.pacman: DirectionAgent = pacman
        self.getCell(self.pacman.pos).setVal(self.pacman.repId)

        self.ghosts: dict[str, GhostAgent] = {REP.BLINKY: blinky, REP.INKY: inky, REP.CLYDE: clyde, REP.PINKY: pinky}
        self.ghostList: List[GhostAgent] = []
        for key, ghost in self.ghosts.items():
            if not ghost is None:
                self.ghostList.append(ghost)
                self.getCell(ghost.pos).setVal(ghost.repId)

        # state cell connections
        # loop connection
        self.getCell(POS.LOOP_POS[0]).setAdj(DIR.LF, self.getCell(POS.LOOP_POS[1]))
        self.getCell(POS.LOOP_POS[1]).setAdj(DIR.RT, self.getCell(POS.LOOP_POS[0]))

        # normal cell connection
        for row in self.state:
            for cell in row:
                if REP.isWall(cell.val):
                    continue

                for dirVal in DIR.getList():
                    newLoc: CPair = cell.coords.move(dirVal)
                    if (
                        newLoc.row > -1
                        and newLoc.col > -1
                        and newLoc.row < BOARD.ROW
                        and newLoc.col < BOARD.COL
                        and BOARD.DATA[newLoc.row][newLoc.col] != REP.WALL
                    ):
                        cell.setAdj(dirVal, self.state[newLoc.row][newLoc.col])

        # pathfinder
        self.pf: PathFinder = PathFinder(self.state)

        # canvas object
        self.canvas: Canvas = None

        self.lastPelletId: int = -1
        self.lastPwrPltId: int = -1

    def setCanvas(self, canvas: Canvas) -> None:
        self.canvas = canvas

    def getCell(self, pos: CPair) -> Cell:
        return self.state[pos.row][pos.col]

    def eatPellet(self, pos: CPair) -> int:
        posStr: str = pos.__str__()
        if posStr in self.pellets:
            pellet: Pellet = self.pellets[posStr]

            if pellet.valid:
                self.getCell(pos).setVal(REP.EMPTY)
                self.pelletProgress -= 1

                return pellet.destroy()

        return 0

    def eatPwrPlt(self, pos: CPair) -> int:
        posStr: str = pos.__str__()
        if posStr in self.pwrplts:
            pellet: Pellet = self.pwrplts[posStr]

            if pellet.valid:
                self.getCell(pos).setVal(REP.EMPTY)
                self.pwrpltEffectCounter = DATA.GHOST_FRIGHTENED_STEP_COUNT

                return pellet.destroy()

        return 0

    def movePacman(self, pos: CPair, pPos: CPair) -> None:
        cell: Cell = self.getCell(pos)
        pCell: Cell = self.getCell(pPos)

        cell.setVal(pCell.val)
        pCell.setVal(REP.EMPTY)

    def moveGhost(self, pos: CPair, pPos: CPair) -> None:
        cell: Cell = self.getCell(pos)
        pCell: Cell = self.getCell(pPos)

        cell.setVal(pCell.val)

        # replenish pellet value to old cell
        pPosStr: str = pCell.__str__()
        if pPosStr in self.pellets and self.pellets[pPosStr].valid:
            pCell.setVal(REP.PELLET)
        elif pPosStr in self.pwrplts and self.pwrplts[pPosStr].valid:
            pCell.setVal(REP.PWRPLT)
        else:
            pCell.setVal(REP.EMPTY)

    # proceed to next time step
    def nextStep(self):
        # timestep management
        self.timesteps += 1

        if self.pwrpltEffectCounter > 0:
            self.pwrpltEffectCounter -= 1


        self.lastPelletId = -1
        self.lastPwrPltId = -1

        # update pacman location
        pPos, pPrevPos, pacmanMoved = self.pacman.getNextPos(self)
        if pacmanMoved:
            self.movePacman(pPos, pPrevPos)

            self.lastPelletId: int = self.eatPellet(pPos)
            if self.canvas != None:
                self.canvas.delete(self.lastPelletId)

            if self.enablePwrPlt:
                self.lastPwrPltId: int = self.eatPwrPlt(pPos)
                if self.canvas != None:
                    self.canvas.delete(self.lastPwrPltId)

        return False, self.pelletProgress == 0
