from typing import List, Tuple

from data import REP
from game.components.movable.ghosts.ghost import Ghost
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Pinky(Ghost):
    def __init__(self, pos: CPair, inHouse: bool, pathfinder: PathFinder) -> None:
        super().__init__(pos, REP.PINKY, inHouse, pathfinder)

    # get target tile of ghost
    def getTargetTile(self, state: List[List[int]]) -> CPair:
        return super().getTargetTile(state)
