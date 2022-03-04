from __future__ import annotations
from typing import List

from utils.direction import DIR


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

    # get manhattan distance
    def manDist(self, cpair: CPair) -> int:
        return abs(self.row - cpair.row) + abs(self.col - cpair.col)

    # custom string representation
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "({}, {})".format(self.row, self.col)

    # custom equal function
    def __eq__(self, o: CPair) -> bool:
        return self.row == o.row and self.col == o.col

    # custom comparator - only used in pathfinding
    def __lt__(self, o: CPair) -> bool:
        return False
