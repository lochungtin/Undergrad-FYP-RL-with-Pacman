from utils.coordinate import CPair


class Component:
    def __init__(self, pos: CPair, repId: int) -> None:
        self.pos: CPair = pos
        self.repId: int = repId

    def setCanvasItemId(self, id: int) -> None:
        self.canvasItemId: int = id
