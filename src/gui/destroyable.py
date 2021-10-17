class Destroyable:
    def __init__(self, canvasItemId: int) -> None:
        self.valid: bool = True
        self.canvasItemId: int = canvasItemId

    # set item validity to false
    def destroy(self) -> int:
        self.valid: bool = False
        return self.canvasItemId
