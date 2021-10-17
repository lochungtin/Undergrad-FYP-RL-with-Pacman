from typing import List

from data import BOARD


class CPair:
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col

    # check if coordinate is valid
    def isValid(self) -> bool:
        return (
            self.row >= 0
            and self.col >= 0
            and self.row < BOARD.row
            and self.col < BOARD.col
        )


    # get all valid neighbouring coordinates
    def getValidNeighbours(self) -> List[CPair]:
        rt: List[CPair] = []

        for neighbour in [
            CPair(self.row + 1, self.col),
            CPair(self.row - 1, self.col),
            CPair(self.row, self.col + 1),
            CPair(self.row, self.col - 1),
        ]:
            if neighbour.isValid:
                rt.append(neighbour)

        return rt
