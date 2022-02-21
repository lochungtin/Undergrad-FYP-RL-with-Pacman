from typing import List
from data.config import CONFIG
from data.data import DATA, REP

from game.components.pellet import Pellet, PowerPellet
from game.utils.state.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR


class State:
    def __init__(self, enabledPwrPlt: bool = True) -> None:
        # fill grid
        self.grid: List[List[Cell]] = []

        # pellets
        self.pellets: dict[str, Pellet] = {}
        self.pelletProgress: int = DATA.TOTAL_PELLET_COUNT

        self.pwrplts: dict[str, PowerPellet] = {}
        self.pwrpltEffectCounter: int = 0

        for i, row in enumerate(CONFIG.BOARD):
            for j, val in enumerate(row):
                cell = Cell(i, j, val)
                self.grid[i][j] = cell

                if val == REP.PELLET:
                    self.pellets[cell.coords.__str__()] = Pellet(cell.coords)
                elif val == REP.PWRPLT and enabledPwrPlt:
                    self.pwrplts[cell.coords.__str__()] = PowerPellet(cell.coords)

        # make connections
        for row in self.grid:
            for cell in row:
                if REP.isWall(cell.val):
                    continue

                for dirVal in DIR.getList():
                    newLoc: CPair = cell.coords.move(dirVal)
                    if newLoc.isValid() and not REP.isWall(CONFIG.BOARD[newLoc.row][newLoc.col]):
                        cell.setAdj(dirVal, self.grid[newLoc.row][newLoc.col])

    def getCell(self, pos: CPair) -> Cell:
        return self.grid[pos.row][pos.col]    

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

    def pacmanMove(self, pos: CPair, pPos: CPair) -> bool:
        if pos == pPos:
            return False

        cell: Cell = self.getCell(pos)
        pCell: Cell = self.getCell(pPos)

        cell.setVal(pCell.val)
        pCell.setVal(REP.EMPTY)

        return True

    def moveGhost(self, pos: CPair, pPos: CPair) -> bool:
        if pos == pPos:
            return False

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

        return True 

    # return 2d array of grid values
    def getRawState(self) -> List[List[int]]:
        return [[cell.val for cell in row] for row in self.grid]
