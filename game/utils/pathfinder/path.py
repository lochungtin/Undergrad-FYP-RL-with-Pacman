from typing import List
from gui.destroyable import Destroyable
from utils.coordinate import CPair


class Path(Destroyable):
    def __init__(self) -> None:
        self.path: List[CPair] = []

    # insert cell to beginning of path
    def insert(self, cpair: CPair) -> None:
        self.path.insert(0, cpair)

    # custom string representation
    def __str__(self) -> str:
        return " -> ".join(str(p) for p in self.path)

    def __repr__(self) -> str:
        return " -> ".join(str(p) for p in self.path)
