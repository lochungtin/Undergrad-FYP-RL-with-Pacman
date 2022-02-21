from copy import deepcopy
from tkinter import Canvas
from typing import List, Tuple

from agents.base import DirectionAgent, GhostAgent
from data.config import CONFIG
from data.data import BOARD, DATA, POS, REP
from game.components.pellet import Pellet, PowerPellet, PelletType
from game.utils.pathfinder.pathfinder import PathFinder
from game.utils.state.cell import Cell
from game.utils.state.state import State
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

        for i, row in enumerate(CONFIG.BOARD):
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
            if hasattr(ghost, "pos"):
                self.ghostList.append(ghost)
                self.getCell(ghost.pos).setVal(ghost.repId)

        # state cell connections
        # loop connection
        self.getCell(CONFIG.LOOP_POS[0]).setAdj(DIR.LF, self.getCell(CONFIG.LOOP_POS[1]))
        self.getCell(CONFIG.LOOP_POS[1]).setAdj(DIR.RT, self.getCell(CONFIG.LOOP_POS[0]))

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
                        and newLoc.row < BOARD.row
                        and newLoc.col < BOARD.col
                        and CONFIG.BOARD[newLoc.row][newLoc.col] != REP.WALL
                    ):
                        cell.setAdj(dirVal, self.state[newLoc.row][newLoc.col])

    def setCanvas(self, canvas: Canvas) -> None:
        self.canvas = canvas

    def getCell(self, pos: CPair) -> Cell:
        return self.state[pos.row][pos.col]

    # proceed to next time step
    def nextStep(self) -> Tuple[bool, bool, bool, bool]:
        self.timesteps += 1

        # update pacman location
        pPos, pPrevPos, pacmanMoved = self.pacman.getNextPos(self)
        if pacmanMoved:
            self.state.movePacman(pPos, pPrevPos)

            displayId: int = self.state.eatPellet(pPos)
            if self.canvas != None:
                self.canvas.delete(displayId)

            if self.enablePwrPlt:
                displayId = self.state.eatPwrPlt(pPos)
                if self.canvas != None:
                    self.canvas.delete(displayId)
