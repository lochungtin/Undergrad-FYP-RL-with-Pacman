from tkinter import Canvas, Tk
from typing import Tuple

from gene import NodeType
from neat.utils import GenomeUtils

BACKGROUND: str = "#1E1E1E"
LINE_S: str = "#909090"
LINE_W: str = "#404040"
NODE: str = "#6BF2C7"
NODE_I: str = "#71c8E3"
NODE_O: str = "#E36685"
LABEL: str = "#FFFFFF"

DIM: int = 960
RADIUS: int = 10
SCALE: int = 45
WIDTH: int = 1.5


class Visualiser:
    def __init__(self) -> None:
        # create gui
        self.main: Tk = Tk()
        self.main.title("Neural Network Visualisation")
        self.canvas: Canvas = Canvas(
            self.main,
            width=DIM,
            height=DIM,
            background=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

    # load neural network from data file
    def load(self, filename: str) -> None:
        # load data
        self.raw: dict[str, object] = GenomeUtils.load(filename, True)
        self.data: dict[int, object] = {}

        maxSize: int = 0
        for (layer, nodes) in self.raw["layers"].items():
            l: int = len(nodes)
            if maxSize < l:
                maxSize = l

        xSize: int = len(self.raw["layers"]) - 1
        xCenter: float = xSize / 2
        for (layer, nodes) in self.raw["layers"].items():
            xRel: float = int(layer) - xCenter

            ySize: int = len(nodes) - 1
            yCenter: float = ySize / 2

            for i, node in enumerate(nodes):
                yRel: float = i - yCenter
                self.data[node] = (
                    DIM / 2 + xRel * SCALE,
                    DIM / 2 + yRel * SCALE * (maxSize / (ySize + 1)),
                )

    # draw neural network and create window
    def display(self) -> None:
        for (key, conns) in self.raw["conns"].items():
            color: str = LINE_W
            if conns["enabled"]:
                color = LINE_S

            n1, n2 = key.split("-")
            node1: Tuple[int, int] = self.data[int(n1)]
            node2: Tuple[int, int] = self.data[int(n2)]

            self.canvas.create_line(node1[0], node1[1], node2[0], node2[1], fill=color, width=WIDTH)

        # draw nodes
        for (key, node) in self.raw["nodes"].items():
            color: str = NODE
            if node["type"] == NodeType.INPUT:
                color = NODE_I
            elif node["type"] == NodeType.OUTPUT:
                color = NODE_O

            pos: Tuple[int, int] = self.data[int(key)]
            # draw circle
            self.drawCircle(pos, color)

            # draw node id
            self.canvas.create_text(pos[0], pos[1], text=node["id"], fill=LABEL, font=("Arial", 8))

        self.main.mainloop()

    # draw circle
    def drawCircle(self, position: Tuple[int, int], color: str) -> None:
        self.canvas.create_oval(
            position[0] - RADIUS,
            position[1] - RADIUS,
            position[0] + RADIUS,
            position[1] + RADIUS,
            fill=BACKGROUND,
            outline=color,
            width=WIDTH,
        )


if __name__ == "__main__":
    filename: str = "./saves/blinky/ne_genome_avgc33.json"
    viz: Visualiser = Visualiser()
    viz.load(filename)
    viz.display()
