from __future__ import annotations
from typing import List

from data import BOARD, DIR


class CPair:
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col

    # translate coordinate according to direction
    def move(self, dir: int) -> CPair:
        if dir == DIR.UP:
            return CPair(self.row - 1, self.col)
        elif dir == DIR.DW:
            return CPair(self.row + 1, self.col)
        elif dir == DIR.LF:
            return CPair(self.row, self.col - 1)
        else:
            return CPair(self.row, self.col + 1)

    # check if coordinate is valid
    def isValid(self) -> bool:
        return (
            self.row >= 0
            and self.col >= 0
            and self.row < BOARD.row
            and self.col < BOARD.col
        )

    # get all valid neighbouring coordinates
    def getValidNeighbours(self) -> List[CPair]:
        rt: List[CPair] = []

        for neighbour in [
            CPair(self.row + 1, self.col),
            CPair(self.row - 1, self.col),
            CPair(self.row, self.col + 1),
            CPair(self.row, self.col - 1),
        ]:
            if neighbour.isValid():
                rt.append(neighbour)

        return rt

    # custom string representation
    def __str__(self) -> str:
        return "({}, {})".format(self.row, self.col)

    def __repr__(self) -> str:
        return "({}, {})".format(self.row, self.col)
