from typing import List
from data import REP
from game.utils.path import Path
from utils.coordinate import CPair


class PathFinder:
    def __init__(self) -> None:
        self.state: List[List[int]] = REP.BOARD

    def reconstructPath() -> Path:
        return Path()
