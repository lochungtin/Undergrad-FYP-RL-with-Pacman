from typing import List, Tuple

from data.config import BOARD

# ghost ai modes
class GHOST_MODE:
    CHASE: int = 0
    SCATTER: int = 1
    FRIGHTENED: int = 2
    DEAD: int = 3

    # blinky
    CRUISE_ELROY: int = 4

    # triggers and mode schedules
    GHOST_EXIT_INTERVAL: int = 3

    GHOST_FRIGHTENED_SPEED_REDUCTION_RATE: int = 3
    GHOST_FRIGHTENED_STEP_COUNT: int = 7

    GHOST_MODE_SCHEDULE: List[Tuple[int, int]] = [
        (SCATTER, 10),
        (CHASE, 15),
        (SCATTER, 7),
        (CHASE, 17),
        (SCATTER, 5),
        (CHASE, 19),
        (SCATTER, 1),
        (CHASE, -1),
    ]


# pixel values of components
class DIM:
    # grid cell and gap size
    JUMP: int = 30
    CELL: int = 25
    GAP: int = 5

    # canvas pixel count
    GBL_H: int = BOARD.ROW * JUMP - GAP
    GBL_W: int = BOARD.COL * JUMP - GAP

    # padding for objects
    PAD_PELLET: int = 9
    PAD_PWRPLT: int = 5
    PAD_DOOR: int = 8


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


# agent class types
class AGENT_CLASS_TYPE:
    # none type (doesnt exist)
    NONE: int = -1
    # playable type (pacman main)
    CTRL: int = 0
    # original type (ghost variant 1)
    OGNL: int = 1
    # hyper-aggressive type (ghost variant 2)
    AGGR: int = 2
    # simple mdp type (pretraining)
    SMDP: int = 3
    # guided deep q learning type (ghost variant 3)
    GDQL: int = 4
    # neuroevolution of augmenting topologies type (ghost variant 4)
    NEAT: int = 5
    # static type (ghost placeholder)
    STTC: int = 6
    # random flag
    RAND: int = 7
