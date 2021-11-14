from __future__ import annotations
from copy import deepcopy
from random import uniform
from typing import List, Tuple

from ai.predictable import Predictable
from ai.neat.gene import Gene


class Genome(Predictable):
    def __init__(self, inNo: int, outNo: int) -> None:
        self.genes: dict[int, Gene] = {}

        self.inNo: int = inNo
        self.outNo: int = outNo

        self.baseNodeCount: int = inNo * outNo

        self.maxInnov: int = 0

        self.fitness: float = 0
        self.speciesIndex: int = -1

    # create copy of itself
    def duplicate(self) -> Genome:
        return deepcopy(self)

    # initialise first population
    def baseInit(self):
        for i in range(self.inNo):
            for o in range(self.outNo):
                self.genes[i * self.outNo + o + 1] = Gene(
                    i + 1,
                    self.inNo + o + 1,
                    uniform(-1, 1),
                    True,
                    i * self.outNo + o + 1,
                )

        self.maxInnov = self.inNo * self.outNo

    # add gene manually
    def addGene(self, gene: Gene) -> None:
        self.genes[gene.innov] = gene

        self.maxInnov = gene.innov

    # find the gene with given params
    def findGene(self, io: Tuple[int, int]) -> Gene:
        for _, (_, gene) in enumerate(self.genes.items()):
            if gene.inNode == io[0] and gene.outNode == io[1]:
                return gene

        return None

    # get gene, return None of no innov id
    def getGene(self, innov: int) -> Gene:
        if innov in self.genes:
            return self.genes[innov]

        return None

    # predict
    def predict(self, input: List[int]) -> List[float]:
        nodes: dict[int, dict[str, object]] = {}

        for _, (_, gene) in enumerate(self.genes.items()):
            if not gene.inNode in nodes:
                nodes[gene.inNode] = {"o": None, "p": []}
            if not gene.outNode in nodes:
                nodes[gene.outNode] = {"o": None, "p": []}

            if gene.enabled:
                nodes[gene.outNode]["p"].append((gene.inNode, gene.weight))

        for i, inputVal in enumerate(input):
            nodes[i + 1]["o"] = inputVal

        rt: List[float] = []
        for i in range(self.inNo + 1, self.inNo + self.outNo + 1):
            rt.append(self.compute(i, nodes))

        return rt

    # compute the output of node (dynamic programming)
    def compute(self, node: int, nodes: dict[int, dict[str, object]]):
        if nodes[node]["o"] != None:
            return nodes[node]["o"]
        else:
            val = 0
            for pair in nodes[node]["p"]:
                val += self.compute(pair[0], nodes) * pair[1]

            nodes[node]["o"] = val
            return val

    # mutation methods
    # add new node
    def addNode(self, inNode: int, outNode: int, nodeId: int, innov: int) -> None:
        ogG: Gene = self.findGene((inNode, outNode))

        ogG.enabled = False

        self.genes[innov - 1] = Gene(inNode, nodeId, ogG.weight, True, innov - 1)
        self.genes[innov] = Gene(nodeId, outNode, 1.0, True, innov)

        self.maxInnov = innov

    # add new connection
    def addConn(self, inNode: int, outNode: int, innov: int) -> None:
        self.genes[innov] = Gene(inNode, outNode, uniform(-1, 1), True, innov)

        self.maxInnov = innov

    # change weight of connection
    def chgWght(self, innov: int, weight: float) -> None:
        self.genes[innov].weight = weight

    # change connection status (enable / disable)
    def chgConn(self, innov: int, enabled: bool) -> None:
        self.genes[innov].enabled = enabled

    # for debugging purposes
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        sb = "<\n"

        for _, (_, gene) in enumerate(self.genes.items()):
            sb += str(gene) + "\n"

        return sb + ">"
