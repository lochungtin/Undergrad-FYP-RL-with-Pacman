from constants import *


class Pacman:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.prevPos = (x, y)
        self.direction = DIR.UP

        self.displayDx = 0
        self.displayDy = 0

    def setDir(self, direction):
        self.direction = direction

    def setDiplayObj(self, obj):
        self.diplay = obj

    def getDisplayDelta(self):
        return self.displayDx, self.displayDy

    def isValidPos(self, pos):
        return pos[1] > -1 and pos[1] < BOARD.col and pos[0] > -1 and pos[0] < BOARD.row

    def nextPos(self, state):
        if self.direction == DIR.UP:
            nextPos = (self.pos[0] - 1, self.pos[1])
            self.displayDx = 0
            self.displayDy = -DIM.JUMP

        elif self.direction == DIR.DW:
            nextPos = (self.pos[0] + 1, self.pos[1])
            self.displayDx = 0
            self.displayDy = DIM.JUMP

        elif self.direction == DIR.RT:
            nextPos = (self.pos[0], self.pos[1] - 1)
            self.displayDx = DIM.JUMP
            self.displayDy = 0

        else:
            nextPos = (self.pos[0], self.pos[1] + 1)
            self.displayDx = -DIM.JUMP
            self.displayDy = 0

        # loop case left
        if nextPos == (14, -1):
            self.prevPos = (14, 0)
            self.pos = (14, 26)

            self.displayDx = -DIM.JUMP * 26
            self.displayDy = 0

            return self.prevPos, self.pos

        # loop case right
        if nextPos == (14, 27):
            self.prevPos = (14, 26)
            self.pos = (14, 0)

            self.displayDx = DIM.JUMP * 26
            self.displayDy = 0

            return self.prevPos, self.pos
        
        # default movement
        if (
            self.isValidPos(nextPos)
            and state[nextPos[0]][nextPos[1]] != 1
            and state[nextPos[0]][nextPos[1]] != 2
        ):
            self.prevPos = self.pos
            self.pos = nextPos
        else:
            self.displayDx = 0
            self.displayDy = 0

        return self.prevPos, self.pos
