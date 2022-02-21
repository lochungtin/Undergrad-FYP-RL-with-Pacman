from typing import List

from game.utils.graph.vertex import Vertex


class Graph:
    def __init__(self) -> None:
        self.vertices: dict[str, Vertex] = {}