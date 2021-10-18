from typing import List
from gui.destroyable import Destroyable
from utils.coordinate import CPair


class Path(Destroyable):
    def __init__(self) -> None:
        self.path: List[CPair] = []

    # append cell to end of path
    def appendCell(self, cpair: CPair) -> None:
        self.path.append(cpair)
