from constants import *
from displayable import Displayable

class Pellet(Displayable):
    def __init__(self, pos, rep):
        super().__init__(pos, rep)

        self.score = pow(10, rep - 1)
        self.isSpecial = rep == REP.PWRPLT
    