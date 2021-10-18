from typing import List
from data import REP
from utils.coordinate import CPair


class PathFinder:
    def __init__(self) -> None:
        self.state: List[List[int]] = REP.BOARD


class PathFinderCell:
    def __init__(self) -> None:
        self.f: int = -1
        self.g: int = -1
        self.h: int = -1
        self.parent: CPair = CPair(-1, -1)