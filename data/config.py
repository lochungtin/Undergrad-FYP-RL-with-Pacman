from typing import List, Tuple

from utils.coordinate import CPair


class BOARD:
    DATA: List[List[int]] = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1],
        [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 4, 1],
        [1, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 1],
        [1, 3, 1, 3, 1, 1, 2, 1, 1, 3, 1, 3, 1],
        [1, 3, 3, 3, 1, 0, 0, 0, 1, 3, 3, 3, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 1],
        [1, 3, 1, 3, 1, 0, 1, 0, 1, 3, 1, 3, 1],
        [1, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 1],
        [1, 4, 1, 1, 1, 3, 1, 3, 1, 1, 1, 3, 1],
        [1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    ROW = len(DATA)
    COL = len(DATA[0])

    MAX_DIST = 23

    TOTAL_PELLET_COUNT: int = 68
    TOTAL_PWRPLT_COUNT: int = 2

    CRUISE_ELROY_TRIGGER: int = 12

    def isValidPos(pos: CPair):
        return pos.row > -1 and pos.col > -1 and pos.row < BOARD.ROW and pos.col < BOARD.COL


class POS:
    # initial pacman location
    PACMAN: CPair = CPair(9, 6)

    # initial ghost locations
    BLINKY: CPair = CPair(5, 6)
    INKY: CPair = CPair(6, 5)
    CLYDE: CPair = CPair(6, 6)
    PINKY: CPair = CPair(6, 7)

    # special locations
    # ghost house reset location
    GHOST_HOUSE_CENTER: CPair = CPair(6, 6)

    # scatter mode target corners
    BLINKY_CORNER: CPair = CPair(1, 1)
    INKY_CORNER: CPair = CPair(13, 1)
    CLYDE_CORNER: CPair = CPair(13, 11)
    PINKY_CORNER: CPair = CPair(1, 11)

    # loop tunnel location
    LOOP_POS: Tuple[CPair, CPair] = (CPair(7, 0), CPair(7, 12))

    # positions where the up direction is not allowed for ghosts
    GHOST_NO_UP_CELLS: List[CPair] = [CPair(3, 5), CPair(3, 7), CPair(10, 5), CPair(10, 7)]

    # ghost house entrace, forbid pacman to enter
    GHOST_HOUSE_ENTRANCE: CPair = CPair(4, 6)
