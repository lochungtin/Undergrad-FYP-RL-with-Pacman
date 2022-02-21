from typing import List, Tuple

from utils.coordinate import CPair



class CONFIG:
    # board pattern for path and walls
    BOARD: List[List[int]] = [
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

    # loop tunnel location
    LOOP_POS: Tuple[CPair, CPair] = (CPair(7, 0), CPair(7, 12))

    # positions where the up direction is not allowed for ghosts
    GHOST_NO_UP_CELLS: List[CPair] = [CPair(3, 5), CPair(3, 7), CPair(10, 5), CPair(10, 7)]

    # ghost house entrace, forbid pacman to enter
    GHOST_HOUSE_ENTRANCE: CPair = CPair(4, 6)
