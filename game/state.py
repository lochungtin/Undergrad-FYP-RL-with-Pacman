from typing import List

from game.components.pellet import Pellet


class State:
    def __init__(self, config: List[List[int]]) -> None:
        self.grid: List[List[int]] = []
        self.graph: 