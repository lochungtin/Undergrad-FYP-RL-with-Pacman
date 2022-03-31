from copy import deepcopy

from gui.displayable import Displayable
from utils.coordinate import CPair


# displayable game component game class
class Component(Displayable):
    def __init__(self, pos: CPair, repId: int) -> None:
        self.pos: CPair = deepcopy(pos)
        self.repId: int = repId
