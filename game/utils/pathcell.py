from utils.coordinate import CPair


class PathCell:
    def __init__(self) -> None:
        self.f: int = -1
        self.g: int = -1
        self.h: int = -1
        self.parent: CPair = CPair(-1, -1)
