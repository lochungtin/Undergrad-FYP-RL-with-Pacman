from typing import List, Tuple


# dimension values of the board
class BOARD:
    row: int = 15
    col: int = 13


# ghost ai modes
class GHOST_MODE:
    CHASE: int = 0
    SCATTER: int = 1
    FRIGHTENED: int = 2
    DEAD: int = 3

    # blinky
    CRUISE_ELROY: int = 4


# game related data constants
class DATA:
    # number of pellets
    TOTAL_PELLET_COUNT: int = 66
    TOTAL_PWRPLT_COUNT: int = 2

    CRUISE_ELROY_TRIGGER: int = 12

    # ghost mode and step counter
    TOTAL_STEP_COUNT: int = 84

    GHOST_EXIT_INTERVAL: int = 3

    GHOST_FRIGHTENED_SPEED_REDUCTION_RATE: int = 3
    GHOST_FRIGHTENED_STEP_COUNT: int = 10
    GHOST_MODE_SCHEDULE: List[Tuple[int, int]] = [
        (GHOST_MODE.SCATTER, 77),
        (GHOST_MODE.CHASE, 57),
        (GHOST_MODE.SCATTER, 50),
        (GHOST_MODE.CHASE, 30),
        (GHOST_MODE.SCATTER, 25),
        (GHOST_MODE.CHASE, 5),
        (GHOST_MODE.SCATTER, 0),
        (GHOST_MODE.CHASE, -1),
    ]


# pixel values of components
class DIM:
    # grid cell and gap size
    JUMP: int = 30
    CELL: int = 25
    GAP: int = 5

    # canvas pixel count
    GBL_H: int = BOARD.row * JUMP - GAP
    GBL_W: int = BOARD.col * JUMP - GAP

    # padding for objects
    PAD_PELLET: int = 9
    PAD_PWRPLT: int = 5
    PAD_DOOR: int = 8


# directions of movement
class DIR:
    UP: int = 0
    DW: int = 1
    LF: int = 2
    RT: int = 3

    def getOpposite(dir: int) -> int:
        if dir == DIR.UP:
            return DIR.DW
        elif dir == DIR.DW:
            return DIR.UP
        elif dir == DIR.LF:
            return DIR.RT
        return DIR.LF


# initial position of displayables
from utils.coordinate import CPair


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

    # loop triggers
    LEFT_LOOP_TRIGGER: CPair = CPair(7, -1)
    LEFT_LOOP: CPair = CPair(7, 0)

    RIGHT_LOOP_TRIGGER: CPair = CPair(7, 13)
    RIGHT_LOOP: CPair = CPair(7, 12)

    # "no go up" zones
    GHOST_NO_UP_1: CPair = CPair(3, 5)
    GHOST_NO_UP_2: CPair = CPair(3, 7)
    GHOST_NO_UP_3: CPair = CPair(10, 5)
    GHOST_NO_UP_4: CPair = CPair(10, 7)


# state representations
class REP:
    BG: int = 0
    EMPTY: int = 0
    WALL: int = 1
    DOOR: int = 2
    PELLET: int = 3
    PWRPLT: int = 4
    PACMAN: int = 5
    BLINKY: int = 6
    INKY: int = 7
    PINKY: int = 8
    CLYDE: int = 9
    FRIGHTENED: int = 10
    DEAD: int = 11

    def isWall(rep: int) -> bool:
        return rep == 1 or rep == 2

    def isPellet(rep: int) -> bool:
        return rep == 3 or rep == 4

    def isGhost(rep: int) -> bool:
        return rep > 5 and rep < 10
