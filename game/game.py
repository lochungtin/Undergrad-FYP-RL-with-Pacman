from tkinter import Canvas
from typing import List, Tuple

from agents.base import DirectionAgent, GhostAgent
from data.config import BOARD, POS
from data.data import DATA, GHOST_MODE, REP
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

        self.ghostModeIndex: int = 0
        self.ghostMode: int = DATA.GHOST_MODE_SCHEDULE[self.ghostModeIndex][0]
        self.ghostModeCounter: int = DATA.GHOST_MODE_SCHEDULE[self.ghostModeIndex][1]

        # state cell connections
        # loop connection
        self.getCell(POS.LOOP_POS[0]).setAdj(DIR.LF, self.getCell(POS.LOOP_POS[1]))
        self.getCell(POS.LOOP_POS[1]).setAdj(DIR.RT, self.getCell(POS.LOOP_POS[0]))

        # normal cell connection
        for row in self.state:
            for cell in row:
                if cell.val == REP.WALL:
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
                self.getCell(pos).setVal(REP.EMPTY)
                self.pelletProgress -= 1

                return pellet.destroy()

        return -1

    def eatPwrPlt(self, pos: CPair) -> int:
        posStr: str = pos.__str__()
        if posStr in self.pwrplts:
            pellet: Pellet = self.pwrplts[posStr]

            if pellet.valid:
                self.getCell(pos).setVal(REP.EMPTY)
                self.pwrpltEffectCounter = DATA.GHOST_FRIGHTENED_STEP_COUNT

                return pellet.destroy()

        return -1

    # handle agent movement
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

    # detect pacman and ghost collision
    def detectCollision(self, pPos: CPair, pPrevPos: CPair, gPos: CPair, gPrevPos: CPair) -> bool:
        print(pPos, pPrevPos, gPos, gPrevPos)
        return pPos == gPos or (pPrevPos == gPos and pPos == gPrevPos)

    # proceed to next time step
    def nextStep(self) -> Tuple[bool, bool]:
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

                self.ghostMode: int = DATA.GHOST_MODE_SCHEDULE[self.ghostModeIndex][0]
                self.ghostModeCounter: int = DATA.GHOST_MODE_SCHEDULE[self.ghostModeIndex][1]

                newGhostMode = True

        self.lastPelletId = -1
        self.lastPwrPltId = -1

        # update pacman location
        pPos, pPrevPos, pMoved = self.pacman.getNextPos(self)
        if pMoved:
            self.movePacman(pPos, pPrevPos)

            self.lastPelletId: int = self.eatPellet(pPos)
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
        for ghost in self.ghostList:
            if newGhostMode:
                if ghost.isClassic:
                    ghost.mode = self.ghostMode

            gPos, gPrevPos, gMoved = ghost.getNextPos(self)
            if gMoved:
                self.moveGhost(gPos, gPrevPos)

            # handle collision
            if self.detectCollision(pPos, pPrevPos, gPos, gPrevPos):
                if not ghost.isDead:
                    if ghost.isFrightened:
                        ghost.isDead = True
                        ghost.isFrightened = False
                    else:
                        return True, self.pelletProgress == 0

        return False, self.pelletProgress == 0
