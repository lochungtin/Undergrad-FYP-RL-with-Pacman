from gui.displayable import Displayable


class Destroyable(Displayable):
    def __init__(self, canvasItemId: int) -> None:
        super().__init__(canvasItemId)

        self.valid: bool = True

    # set item validity to false
    def destroy(self) -> int:
        self.valid: bool = False

        if hasattr(self, "canvasItemId"):
            return self.canvasItemId

        return -1
