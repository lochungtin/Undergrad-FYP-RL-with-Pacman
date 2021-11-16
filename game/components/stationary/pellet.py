from typing import Union
from typing_extensions import TypeAlias
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


# power pellet class
class PowerPellet(Component, Destroyable):
    def __init__(self, pos: CPair) -> None:
        self.pos: CPair = pos
        self.repId: int = REP.PWRPLT

        self.valid: bool = True


# pellet type
PelletType: TypeAlias = Union[Pellet, PowerPellet]
