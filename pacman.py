from constants import *


class Pacman:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.prevPos = (x, y)
        self.direction = DIR.UP

    def setDir(self, direction):
        self.direction = direction

    def isValidPos(self, pos):
        return pos[0] > -1 and pos[0] < BOARD.col and pos[1] > -1 and pos[1] < BOARD.row

    def nextPos(self, state):
        if self.direction == DIR.UP:
            nextPos = (self.pos[0] - 1, self.pos[1])
        elif self.direction == DIR.DW:
            nextPos = (self.pos[0] + 1, self.pos[1])
        elif self.direction == DIR.RT:
            nextPos = (self.pos[0], self.pos[1] - 1)
        else:
            nextPos = (self.pos[0], self.pos[1] + 1)

        # loop case left
        if nextPos == (14, -1):
            self.prevPos = (14, 0)
            self.pos = (14, 26)
            return self.prevPos, self.pos

        # loop case right
        if nextPos == (14, 27):
            self.prevPos = (14, 26)
            self.pos = (14, 0)
            return self.prevPos, self.pos
        
        # default movement
        if (
            self.isValidPos(nextPos)
            and state[nextPos[0]][nextPos[1]] != 1
            and state[nextPos[0]][nextPos[1]] != 2
        ):
            self.prevPos = self.pos
            self.pos = nextPos

        return self.prevPos, self.pos
