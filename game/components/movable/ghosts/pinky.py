from typing import List, Tuple

from data import POS, REP
from game.components.movable.ghosts.ghost import Ghost
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Pinky(Ghost):
    def __init__(self, pathfinder: PathFinder) -> None:
        super().__init__(POS.PINKY, REP.PINKY, True, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        return super().getTargetTile(state)
