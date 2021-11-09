from typing import Callable
import time


class TimeController:
    def __init__(self, stepDuration: int, action: Callable[[], None]) -> None:
        self.stepDuration: int = stepDuration
        self.action: Callable[[], None] = action

        self.running: bool = True
        self.kill: bool = False

    # toggle pause of the loop
    def toggle(self) -> None:
        self.running = not self.running

    # start the controller
    def start(self) -> None:
        while not self.kill:
            if self.running:
                time.sleep(self.stepDuration)

                self.action()

    # kill the controller
    def end(self) -> None:
        self.kill = True
