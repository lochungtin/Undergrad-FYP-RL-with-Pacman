from utils.coordinate import CPair


class PathCell:
    def __init__(self) -> None:
        self.f: float = -1
        self.g: float = -1
        self.h: float = -1
        self.parent: CPair = CPair(-1, -1)

    # update data of cell
    def update(self, f: float, g: float, h: float, parent: CPair) -> None:
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent
