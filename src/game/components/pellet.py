from ...data.constants import *
from .displayable import Displayable

class Pellet(Displayable):
    def __init__(self, pos, rep):
        super().__init__(pos, rep)

        self.score = pow(10, abs(rep - 3))
        self.isSpecial = rep == REP.PWRPLT
        self.valid = True

    def destroy(self):
        self.valid = False
    
