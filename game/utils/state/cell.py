from __future__ import annotations
from typing import List

from utils.direction import DIR


class Cell:
    def makeId(row: int, col: int) -> str:
        return "{},{}".format(row, col)

    def __init__(self, id: str, val: int) -> None:
        self.id: str = id
        self.val: int = val
        self.adj: dict[str, Cell] = {DIR.UP: None, DIR.DW: None, DIR.LF: None, DIR.RT: None}

    def setAdj(self, dir: int, neighbour: Cell) -> None:
        self.adj[dir] = neighbour

    def getNeighbours(self) -> List[Cell]:
        return [node for id, node in self.adj.items()]
