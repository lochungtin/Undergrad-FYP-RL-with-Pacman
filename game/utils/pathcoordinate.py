from __future__ import annotations
from functools import total_ordering

from utils.coordinate import CPair


@total_ordering
class PathCPair(object):
    def __init__(self, cpair: CPair, score: float) -> None:
        self.cpair: CPair = cpair
        self.score: float = score

    # for maintaining order in a priority queue
    def __lt__(self, o: PathCPair) -> bool:
        return self.score < o.score

    def __eq__(self, o: PathCPair) -> bool:
        return self.score == o.score
