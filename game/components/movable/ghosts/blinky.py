from typing import List, Tuple

from data import POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Blinky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.BLINKY, REP.BLINKY, False, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        for rowIndex, row in enumerate(state):
            for colIndex, cell in enumerate(row):
                if cell == REP.PACMAN:
                    targetTile: CPair = CPair(rowIndex, colIndex)

        return targetTile
