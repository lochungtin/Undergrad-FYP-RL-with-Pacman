from ghost import Ghost


class Clyde(Ghost):
    def __init__(self, pos):
        super().__init__(pos)

    def nextPos(self, state):
        return self.prevPos, self.pos
        