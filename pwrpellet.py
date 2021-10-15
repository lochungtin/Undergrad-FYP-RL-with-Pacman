from constants import *
from displayable import Displayable

class PwrPlt(Displayable):
    def __init__(self, pos):
        super().__init__(pos, REP.PWRPLT)

        self.visible = True

    def setVisibility(self, visible):
        self.visible = visible