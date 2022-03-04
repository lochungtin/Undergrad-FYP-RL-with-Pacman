from data.data import REP
from game.components.component import Component
from gui.destroyable import Destroyable
from utils.coordinate import CPair


# pellet class
class Pellet(Component, Destroyable):
    def __init__(self, pos: CPair) -> None:
        self.pos: CPair = pos
        self.repId: int = REP.PELLET

        self.valid: bool = True

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "[id: {}, p: {}, v: {}]".format(self.repId, self.pos, self.valid)


# power pellet class
class PowerPellet(Component, Destroyable):
    def __init__(self, pos: CPair) -> None:
        self.pos: CPair = pos
        self.repId: int = REP.PWRPLT

        self.valid: bool = True

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "[id: {}, p: {}, v: {}]".format(self.repId, self.pos, self.valid)
