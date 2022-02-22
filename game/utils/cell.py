from __future__ import annotations
from copy import deepcopy
from typing import List
from data.data import REP

from utils.coordinate import CPair
from utils.direction import DIR


class Cell:
    def __init__(self, row: int, col: int, val: int) -> None:
        self.coords: CPair = CPair(row, col)
        self.id: str = self.coords.__str__()

        self.adj: dict[int, Cell] = {DIR.UP: None, DIR.DW: None, DIR.LF: None, DIR.RT: None}

        # fixtures
        self.isWall: bool = val == REP.WALL
        self.iSDoor: bool = val == REP.DOOR

        # pellets
        self.hasPellet: bool = val == REP.PELLET
        self.hasPwrplt: bool = val == REP.PWRPLT

        # agents
        self.hasPacman: bool = val == REP.PACMAN
        self.hasGhost: bool = REP.isGhost(val)
        self.ghosts: dict[str, bool] = {
            REP.BLINKY: val == REP.BLINKY,
            REP.INKY: val == REP.INKY,
            REP.CLYDE: val == REP.CLYDE,
            REP.PINKY: val == REP.PINKY,
        }

    def setAdj(self, dir: int, neighbour: Cell) -> None:
        self.adj[dir] = neighbour

    def isIntersection(self) -> bool:
        count: int = 0

        for dir, neighbour in self.adj.items():
            count += (neighbour is None) * 1

        return count < 2

    def occupied(self) -> bool:
        return (self.hasPacman + self.hasPellet + self.hasPwrplt + self.hasGhost) > 0

    def getValidNeighbours(self) -> List[Cell]:
        valids: List[Cell] = []

        for dir, neighbour in self.adj.items():
            if not neighbour is None:
                valids.append(neighbour)

        return valids

    # custom string representation
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        ghostString: str = ""
        for id, ghost in self.ghosts.items():
            ghostString += str(ghost * 1)

        return "{}: [{}, {}, {}, {}]".format(
            self.id,
            self.isWall * 2 + self.isWall,
            self.hasPwrplt * 2 + self.hasPellet,
            self.hasPacman,
            ghostString,
        )
