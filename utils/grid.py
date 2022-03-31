from typing import List

from data.config import BOARD


def createGameSizeGrid(fill = None) -> List[List[object]]:
    return [[fill for j in range(BOARD.COL)] for i in range(BOARD.ROW)]
