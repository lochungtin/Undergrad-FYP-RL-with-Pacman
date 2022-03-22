from random import Random
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base.base import GhostAgent
from data.config import POS
from data.data import GHOST_MODE
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR


# base class for classic ghost agents
class ClassicGhostAgent(GhostAgent):
    def __init__(self, pos: CPair, repId: int, initWait: int) -> None:
        GhostAgent.__init__(self, pos, repId, True)

        # ghost mode
        self.mode: int = GHOST_MODE.SCATTER

        # initial waiting countdown
        self.initWait: int = initWait

        # random state (for set seed analysis)
        self.rand: Random = Random()

    # get regular movement positions
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # start random walk if frightened
        if self.isFrightened and (not hasattr(self, "cruiseElroy") or not self.cruiseElroy):
            # slow down ghost speed
            self.speedReducer = (self.speedReducer + 1) % GHOST_MODE.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE
            if self.speedReducer == 0:
                # filter out valid locations
                valid: List[Cell] = []
                for dir, neighbour in game.state[self.pos.row][self.pos.col].adj.items():
                    if not neighbour is None and not (dir != DIR.UP and self.pos in POS.GHOST_NO_UP_CELLS):
                        valid.append(neighbour)

                # random choice
                self.prevPos = self.pos
                self.pos = self.rand.choice(valid).coords
                self.moved = True

        # regular behaviour
        else:
            # get target tile
            targetTile: CPair = self.getTargetTile(game)

            # looping mechanic
            if self.pos == targetTile:
                targetTile = self.prevPos

            # generate path
            self.prevPath = self.path
            if self.pos != targetTile:
                self.path = self.pathfinder.start(self.pos, targetTile, self.direction)

            # update positions
            self.prevPos = self.pos
            if len(self.path) > 0:
                self.pos = self.path[0]
            self.moved = True

        # update direction of travel
        if self.moved:
            self.direction = self.pos.relate(self.prevPos)

        return self.pos, self.prevPos, self.moved

    # ===== REQUIRED TO OVERRIDE =====
    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        raise NotImplementedError


# placeholder ghost agent
class StaticGhostAgent(GhostAgent):
    def __init__(self, pos: CPair, repId: int) -> None:
        GhostAgent.__init__(self, pos, repId, False)

        self.moved = False

    # return static position
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        return self.pos, self.pos, False
