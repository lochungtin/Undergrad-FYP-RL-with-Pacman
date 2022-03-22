from copy import deepcopy
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from data.config import POS
from game.components.component import Component
from game.utils.cell import Cell
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair
from utils.direction import DIR


# base class for game agents
class Agent(Component):
    def __init__(self, pos: CPair, repId: int) -> None:
        Component.__init__(self, pos, repId)

        self.direction: int = DIR.UP
        self.prevPos: CPair = deepcopy(pos)
        self.moved: bool = True

    # ===== REQUIRED TO OVERRIDE =====
    # get next position of character
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        raise NotImplementedError


# base class for all (pacman and ghosts) direction controllable game agents
class DirectionAgent(Agent):
    def __init__(self, pos: CPair, repId: int) -> None:
        Agent.__init__(self, pos, repId)

    # set direction
    def setDir(self, direction: int) -> None:
        self.direction: int = direction

    # get next position of agent
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        curPos: Cell = game.getCell(self.pos)
        nextPos: Cell = curPos.adj[self.direction]
        self.moved = False

        # check if move is valid
        if nextPos is None:
            return self.pos, self.prevPos, self.moved

        # update data
        self.pos = nextPos.coords
        self.prevPos = curPos.coords
        self.moved = True

        return self.pos, self.prevPos, self.moved


# base class for ghost agents
class GhostAgent(Agent):
    def __init__(self, pos: CPair, repId: int) -> None:
        Agent.__init__(self, pos, repId)

        # ghost states
        self.isDead: bool = False
        self.isFrightened: bool = False
        self.speedReducer: int = 0

        # paths
        self.path: List[CPair] = []
        self.pathId: int = -1

    # bind pathfinder
    def bindPathFinder(self, pathfinder: PathFinder) -> None:
        self.pathfinder: PathFinder = pathfinder

    # get next position of ghost
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        self.moved = False
        # wait at ghost house
        if hasattr(self, "initWait") and self.initWait > 0:
            self.initWait -= 1
            return self.pos, self.pos, self.moved

        # dead and returned to ghost house
        if self.isDead and self.pos == POS.GHOST_HOUSE_CENTER:
            self.isDead = False

        # dead movement sequence
        if self.isDead:
            # generate path
            self.prevPath = self.path
            self.path = self.pathfinder.start(self.pos, POS.GHOST_HOUSE_CENTER, self.direction)

            # update positions
            self.prevPos = self.pos
            if len(self.path) > 0:
                self.pos = self.path[0]
            self.moved = True

            if self.moved:
                self.direction = self.pos.relate(self.prevPos)

            return self.pos, self.prevPos, self.moved

        # regular movement sequence
        else:
            return self.regularMovement(game)

    # ===== REQUIRED TO OVERRIDE =====
    # get regular movement positions
    def regularMovement(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        raise NotImplementedError()
