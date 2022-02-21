from __future__ import annotations
from copy import deepcopy

from utils.coordinate import CPair
from utils.direction import DIR


class Cell:
    def __init__(self, row: int, col: int, val: int) -> None:
        self.coords: CPair = CPair(row, col)
        self.id: str = self.coords.__str__()

        self.val: int = val

        self.adj: dict[int, Cell] = {DIR.UP: None, DIR.DW: None, DIR.LF: None, DIR.RT: None}

    def setVal(self, val: int) -> int:
        old: int = self.val
        self.val = val

        return old

    def setAdj(self, dir: int, neighbour: Cell) -> None:
        self.adj[dir] = neighbour

    def getNeighbours(self) -> dict[int, Cell]:
        return deepcopy(self.adj)

    # custom string representation
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "[{} = {}]".format(self.id, self.val)
