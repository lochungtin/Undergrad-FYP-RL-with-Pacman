from copy import deepcopy
from random import choice
from typing import List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from data.data import DATA, DIR, GHOST_MODE, POS, REP
from game.components.component import Component
from game.utils.pathfinder.path import Path
from game.utils.pathfinder.pathfinder import PathFinder
from utils.coordinate import CPair


# base class for game agents
class Agent(Component):
    def __init__(self, pos: CPair, repId: int) -> None:
        super().__init__(pos, repId)

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
        super().__init__(pos, repId)

    # set direction
    def setDir(self, direction: int) -> None:
        self.direction: int = direction

    # get next position of agent
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        newPos: CPair = self.pos.move(self.direction)
        self.moved = False

        # special cases (looping)
        if newPos == POS.LEFT_LOOP_TRIGGER:
            self.prevPos = self.pos
            self.pos = POS.RIGHT_LOOP
            self.moved = True

        elif newPos == POS.RIGHT_LOOP_TRIGGER:
            self.prevPos = self.pos
            self.pos = POS.LEFT_LOOP
            self.moved = True

        # natural movement
        elif newPos.isValid() and not REP.isWall(game.state[newPos.row][newPos.col]):
            self.prevPos = self.pos
            self.pos = newPos
            self.moved = True

        return self.pos, self.prevPos, self.moved


# base class for ghost agents
class GhostAgent(Agent):
    def __init__(self, pos: CPair, repId: int, isClassic: bool) -> None:
        super().__init__(pos, repId)

        self.isDead: bool = False
        self.isFrightened: bool = False
        self.speedReducer: int = 2

        self.isClassic: bool = isClassic


# base class for classic ghost agents
class ClassicGhostAgent(GhostAgent):
    def __init__(self, pos: CPair, repId: int, initWait: int) -> None:
        super().__init__(pos, repId, True)

        self.mode: int = GHOST_MODE.SCATTER

        self.path: Path = Path()
        self.prevPath: Path = Path()

        self.initWait: int = initWait

    # bind pathfinder
    def bindPathFinder(self, pathFinder: PathFinder) -> None:
        self.pathfinder: PathFinder = pathFinder

    # modified version of getNeighbours to accomodate for "no go up" zones
    def getNeighbours(self, state: List[List[int]]) -> List[CPair]:
        rt: List[CPair] = []

        for index, pos in enumerate(self.pos.getNeighbours()):
            if (
                (
                    pos == POS.GHOST_NO_UP_1
                    or pos == POS.GHOST_NO_UP_2
                    or pos == POS.GHOST_NO_UP_3
                    or pos == POS.GHOST_NO_UP_4
                )
                and index == 0
                or REP.isWall(state[pos.row][pos.col])
                or DIR.getOpposite(self.direction) == index
            ):
                continue

            rt.append(pos)

        return rt

    # get next position of ghost
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # wait at ghost house
        if self.initWait > -1:
            self.initWait -= 1
            return self.pos, self.pos, False

        # dead and returned to ghost house
        if self.isDead and self.pos == POS.GHOST_HOUSE_CENTER:
            self.isDead = False

        # start random walk if frightened
        if self.isFrightened:
            # update prev pos
            self.prevPos = self.pos

            # reverse direction for first step
            # hold position if reverse is invalid
            if self.speedReducer == DATA.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE:
                newPos = self.pos.move(DIR.getOpposite(self.direction))
                if newPos.isValid() and not REP.isWall(game.state[newPos.row][newPos.col]):
                    self.pos = newPos

                self.speedReducer = DATA.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE - 1

            # slow down ghost speed
            self.speedReducer = (self.speedReducer + 1) % DATA.GHOST_FRIGHTENED_SPEED_REDUCTION_RATE
            if self.speedReducer == 0:
                self.pos = choice(self.getNeighbours(game.state))

        # normal behaviour
        else:
            self.updatePositions(game)

        # update direction of travel
        if self.pos != self.prevPos:
            self.direction = self.pos.relate(self.prevPos)

        return self.pos, self.prevPos, True

    # perform normal behaviour for next step
    def updatePositions(self, game: "Game") -> None:
        # get target tile
        targetTile: CPair = self.getTargetTile(game)
        if self.pos == targetTile:
            targetTile = self.prevPos

        # generate path
        self.prevPath = self.path
        if self.pos != targetTile:
            self.path = self.pathfinder.start(self.pos, targetTile, self.direction)

        self.prevPos = self.pos
        if len(self.path.path) > 0:
            self.pos = self.path.path[0]

    # ===== REQUIRED TO OVERRIDE =====
    # get target tile of ghost
    def getTargetTile(self, game: "Game") -> CPair:
        raise NotImplementedError


# base class for all (pacman and ghosts) deep q learning based agents
class DQLAgent(DirectionAgent):
    def __init__(self, pos: CPair, repId: int, neuralNet: NeuralNet) -> None:
        super().__init__(pos, repId)

        self.neuralNet: NeuralNet = neuralNet

    # get next position of agent
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # get action vals
        state: List[int] = self.processGameState(game)
        qVals: List[float] = self.neuralNet.predict(np.array([state]))

        # get optimal action
        action: int = np.argmax(qVals)

        # selection action direction
        self.setDir(action)

        return super().getNextPos(game)

    # ===== REQUIRED TO OVERRIDE =====
    # preprocess game state for neural network
    def processGameState(self, game: "Game") -> List[int]:
        raise NotImplementedError


# base class for all ghost neuro-evolution based agents
class NEATGhostAgent(GhostAgent, DirectionAgent):
    def __init__(self, pos: CPair, repId: int, genome: Genome) -> None:
        GhostAgent().__init__(pos, repId, False)

        self.genome: Genome = genome

    # get next position of ghost
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair, CPair]:
        # get action vals
        state: List[int] = self.processGameState(game.state)
        qVals: List[float] = self.genome.predict(self.processGameState(state))

        # get optimal action
        action: int = np.argmax(qVals)

        # selection action direction
        self.setDir(action)

        return DirectionAgent().getNextPos(game)

    # ===== REQUIRED TO OVERRIDE =====
    # preprocess game state for neural network
    def processGameState(self, state: List[List[int]]) -> List[int]:
        raise NotImplementedError
