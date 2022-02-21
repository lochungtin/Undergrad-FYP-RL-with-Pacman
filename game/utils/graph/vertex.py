from __future__ import annotations
from tkinter import N
from typing import List


class Vertex:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.neighbours: dict[int, Vertex] = {}

    def addNeighbour(self, neighbour: Vertex) -> None:
        self.neighbours[neighbour.id] = neighbour

    def getNeighbours(self) -> List[Vertex]:
        return [node for id, node in self.neighbours.items()]
