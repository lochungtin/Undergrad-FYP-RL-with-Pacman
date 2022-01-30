from random import randint
from typing import List, Tuple

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game

from agents.base import Base, IntelligentBase
from ai.predictable import Predictable
from data.data import BOARD, DIR, GHOST_MODE, POS, REP
from utils.coordinate import CPair


# pacman base agent
class PacmanBaseAgent(Base):
    def __init__(self) -> None:
        super().__init__(POS.PACMAN, REP.PACMAN)


# playable keyboard agent for pacman
class PlayableAgent(PacmanBaseAgent):
    def __init__(self) -> None:
        super().__init__()

        # initialise direction
        self.direction = DIR.UP

    # get next position of pacman
    def getNextPos(self, game: "Game") -> Tuple[CPair, CPair]:
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

        return self.pos, self.prevPos

    # set direction
    def setDir(self, direction: int) -> None:
        self.direction: int = direction


# neat agent for pacman
class NEATAgent(PacmanBaseAgent, IntelligentBase):
    def __init__(self, predictable: Predictable) -> None:
        IntelligentBase.__init__(self, POS.PACMAN, REP.PACMAN, predictable)

    def locComp(self, pov: CPair, loc: CPair) -> List[int]:
        return [
            int(pov.row > loc.row), # should move up
            int(pov.row < loc.row), # should move down
            int(pov.col > loc.col), # should move left
            int(pov.col < loc.col), # should move right
        ]

    def processState(self, game: "Game") -> List[int]:
        input: List[int] = []

        pacPos: CPair = game.pacman.pos
        for dir in [DIR.UP, DIR.DW, DIR.LF, DIR.RT]:
            newPos: CPair = pacPos.move(dir)

            valid: bool = False
            if CPair.isValid(newPos):
                valid = not REP.isWall(game.state[newPos.row][newPos.col])

            input.append(int(valid))

        pltDist: int = 2 * BOARD.row
        pwrDist: int = 2 * BOARD.row

        pltPos: CPair = pacPos
        pwrPos: CPair = pacPos

        for r in range(BOARD.row):
            for c in range(BOARD.col):
                cell = game.state[r][c]
                manDist: int = abs(pacPos.row - r) + abs(pacPos.col - c)

                if cell == REP.PELLET and manDist < pltDist:
                    pltDist = manDist
                    pltPos = CPair(r, c)

                elif cell == REP.PWRPLT and manDist < pwrDist:
                    pwrDist = manDist
                    pwrPos = CPair(r, c)

        pltPos = game.pathfinder.start(pacPos, pltPos, -1).path[0]
        # pwrPos = game.pathfinder.start(pacPos, pwrPos, -1).path[0]

        input += self.locComp(pacPos, pltPos)
        input += self.locComp(pacPos, pwrPos)

        # print(input[0:4], input[4:8], pacPos, pltPos)

        if hasattr(game, "ghosts"):
            for ghost in game.ghosts:
                input.append(int(ghost.pos.row < pacPos.row))
                input.append(int(ghost.pos.row > pacPos.row))
                input.append(int(ghost.pos.col < pacPos.col))
                input.append(int(ghost.pos.col > pacPos.col))
                input.append(int(ghost.isDead))
                input.append(int(ghost.isFrightened))

            input.append(int(game.inky.mode == GHOST_MODE.CHASE))
        else:
            for _ in range(25):
                input.append(0)

        return input
