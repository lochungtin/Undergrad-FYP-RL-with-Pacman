class Destroyable:
    def __init__(self, canvasItemId: int) -> None:
        self.valid: bool = True
        self.canvasItemId: int = canvasItemId

    def destroy(self) -> int:
        self.valid: bool = False
        return self.canvasItemId
