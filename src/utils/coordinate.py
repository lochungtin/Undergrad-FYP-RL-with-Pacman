from ..data import BOARD


class CPair:
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col

    def isValid(self) -> bool:
        return (
            self.row >= 0
            and self.col >= 0
            and self.row < BOARD.row
            and self.col < BOARD.col
        )
