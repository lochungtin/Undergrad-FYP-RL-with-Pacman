from data import *
from movable import Movable


class Pacman(Movable):
    def __init__(self, pos):
        super().__init__(pos, REP.PACMAN)

        self.direction = DIR.UP

    # set direction of travel
    def setDir(self, direction):
        self.direction = direction

    def nextPos(self, state):
        # calculate next position
        if self.direction == DIR.UP:
            nextPos = (self.pos[0] - 1, self.pos[1])
        elif self.direction == DIR.DW:
            nextPos = (self.pos[0] + 1, self.pos[1])
        elif self.direction == DIR.LF:
            nextPos = (self.pos[0], self.pos[1] - 1)
        else:
            nextPos = (self.pos[0], self.pos[1] + 1)

        # loop case left
        if nextPos == (14, -1):
            self.prevPos = (14, 0)
            self.pos = (14, 26)
            self.moved = True

            return self.prevPos, self.pos

        # loop case right
        if nextPos == (14, 27):
            self.prevPos = (14, 26)
            self.pos = (14, 0)
            self.moved = True

            return self.prevPos, self.pos

        # default movement
        self.moved = (
            self.isValidPos(nextPos)
            and state[nextPos[0]][nextPos[1]] != REP.WALL
            and state[nextPos[0]][nextPos[1]] != REP.DOOR
        )
        if self.moved:
            self.prevPos = self.pos
            self.pos = nextPos

        return self.prevPos, self.pos
