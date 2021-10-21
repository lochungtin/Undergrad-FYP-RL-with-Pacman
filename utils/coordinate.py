from __future__ import annotations
from typing import List

from data import BOARD, DIR


class CPair:
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col

    # check if coordinate is valid
    def isValid(self) -> bool:
        return (
            self.row >= 0
            and self.col >= 0
            and self.row < BOARD.row
            and self.col < BOARD.col
        )

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

    # reflect with respect to
    def reflect(self, pivot: CPair) -> CPair:
        dy = pivot.row - self.row
        dx = pivot.col - self.col

        return CPair(self.row + dy, self.col + dx)

    # get direction relation of coordinate pairs
    def relate(self, cpair: CPair) -> int:
        if self.row + 1 == cpair.row and self.col == cpair.col:
            return DIR.UP
        elif self.row - 1 == cpair.row and self.col == cpair.col:
            return DIR.DW
        elif self.row == cpair.row and self.col + 1 == cpair.col:
            return DIR.LF
        elif self.row == cpair.row and self.col - 1 == cpair.col:
            return DIR.RT

        # not a valid comparison
        return -1

    # get all valid neighbouring coordinates
    def getNeighbours(self) -> List[CPair]:
        rt: List[CPair] = []

        for neighbour in [
            CPair(self.row - 1, self.col),
            CPair(self.row + 1, self.col),
            CPair(self.row, self.col - 1),
            CPair(self.row, self.col + 1),
        ]:
            if neighbour == CPair(14, -1):
                rt.append(CPair(14, 26))
            elif neighbour == CPair(14, 27):
                rt.append(CPair(14, 0))
            elif neighbour.isValid():
                rt.append(neighbour)

        return rt

    # custom string representation
    def __str__(self) -> str:
        return "({}, {})".format(self.row, self.col)

    def __repr__(self) -> str:
        return "({}, {})".format(self.row, self.col)

    # custom equal function
    def __eq__(self, o: CPair) -> bool:
        return self.row == o.row and self.col == o.col
