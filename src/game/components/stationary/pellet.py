from ....gui.destroyable import Destroyable
from ..component import Component
from utils.coordinate import CPair

class Pellet(Component, Destroyable):
    def __init__(self, pos: CPair, repId: int) -> None:
        self.pos: CPair = pos
        self.repId: int = repId

class PowerPellet(Component, Destroyable):
    def __init__(self, pos: CPair, repId: int) -> None:
        self.pos: CPair = pos
        self.repId: int = repId
    