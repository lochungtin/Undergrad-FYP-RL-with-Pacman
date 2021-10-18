class Displayable:
    def __init__(self, canvasItemId: int) -> None:
        self.canvasItemId: int = canvasItemId

    # set canvas item id of component
    def setCanvasItemId(self, canvasItemId: int) -> None:
        self.canvasItemId: int = canvasItemId
