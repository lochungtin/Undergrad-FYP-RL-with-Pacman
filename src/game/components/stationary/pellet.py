from typing import Union
from typing_extensions import TypeAlias
from data import REP
from game.components.component import Component
from gui.destroyable import Destroyable
from utils.coordinate import CPair


class Pellet(Component, Destroyable):
    def __init__(self, pos: CPair) -> None:
        self.pos: CPair = pos
        self.repId: int = REP.PELLET


class PowerPellet(Component, Destroyable):
    def __init__(self, pos: CPair) -> None:
        self.pos: CPair = pos
        self.repId: int = REP.PWRPLT


TypePellet: TypeAlias = Union[Pellet, PowerPellet]
