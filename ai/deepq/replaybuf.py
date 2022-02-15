from random import choices
from typing import List


class ReplayBuffer:
    def __init__(self, size: int, batchSize: int) -> None:
        self.buffer: List[List[object]] = []

        self.maxSize: int = size
        self.batchSize: int = batchSize

    def append(self, s: List[int], a: int, r: float, t: int, nS: List[int]) -> None:
        if len(self.buffer) == self.maxSize:
            del self.buffer[0]

        self.buffer.append([s, a, r, t, nS])

    def getSample(self) -> List[List[object]]:
        return choices(self.buffer, k=self.batchSize)

    def isReady(self):
        return len(self.buffer) == self.maxSize
