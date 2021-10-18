from gui.displayable import Displayable
from utils.coordinate import CPair


class Component(Displayable):
    def __init__(self, pos: CPair, repId: int) -> None:
        self.pos: CPair = pos
        self.repId: int = repId
