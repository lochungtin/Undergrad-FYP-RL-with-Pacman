import enum
from typing import List

from game.components.pellet import Pellet
from game.cell import Cell


class State:
    def __init__(self, config: List[List[int]]) -> None:        
        # fill grid
        self.grid: List[List[Cell]] = [[Cell(Cell.makeId(i, j), cell) for j, cell in enumerate(row)] for i, row in enumerate(config)]

        # make connections



    # return 2d array of grid values
    def getRawState(self) -> List[List[int]]:
        return [[cell.val for cell in row] for row in self.grid]
