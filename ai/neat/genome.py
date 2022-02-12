from __future__ import annotations
from copy import deepcopy
from random import choice, randint, random, uniform
from typing import List

from ai.predictable import Predictable
from ai.neat.gene import ConnGene, NodeGene, NodeType


class Genome(Predictable):
    def __init__(self, config: dict[str, object], gen1: bool = False) -> None:
        self.inSize: int = config["inSize"]
        self.outSize: int = config["outSize"]

        # id: gene
        self.nodes: dict[int, NodeGene] = {}
        # key: gene
        self.conns: dict[str, ConnGene] = {}

        # topological structure data
        # id: List[parent Id]
        self.cStruct: dict[int, List[int]] = {}
        self.pStruct: dict[int, List[int]] = {}
        # id: layer
        self.lMap: dict[int, int] = {}
        # layer: List[id]
        self.layers: dict[int, List[int]] = {
            0: [],
            1: [],
        }
        self.layerNum: int = len(self.layers)

        # create IO nodes
        for i in range(self.inSize):
            # create input node
            self.nodes[i] = NodeGene({"id": i, "type": NodeType.INPUT, "bias": 0})

            # maintain topological structure data
            self.cStruct[i] = []

            self.lMap[i] = 0
            self.layers[0].append(i)

        for o in range(self.inSize, self.outSize + self.inSize):
            # create output node
            self.nodes[o] = NodeGene({"id": o, "type": NodeType.OUTPUT, "bias": 0})

            # maintain topological structure data
            self.pStruct[o] = []

            self.lMap[o] = 1
            self.layers[1].append(o)

        # create connections for generation 1
        if gen1:
            for i in range(self.inSize):
                for o in range(self.inSize, self.outSize + self.inSize):
                    key: str = ConnGene.genKey(i, o)
                    self.conns[key] = ConnGene(
                        {
                            "inId": i,
                            "outId": o,
                            "key": key,
                            "weight": uniform(-1, 1),
                            "innov": i * self.outSize + (o - self.inSize),
                        }
                    )

                    # maintain topological structure data
                    self.cStruct[i].append(o)
                    self.pStruct[o].append(i)

    # evaluate neural net - predict actino values
    def predict(self, input: List[float]) -> List[float]:
        if len(input) != self.inSize:
            return None

        outputList: dict[int, float] = {}
        for idx, val in enumerate(input):
            outputList[idx] = val

        return [self.evalRec(i, outputList) for i in range(self.inSize, self.outSize + self.inSize)]

    def evalRec(self, id: int, outputList: dict[int, float]) -> float:
        if id in outputList:
            return outputList[id]
        else:
            # ignore unconnected nodes
            if id not in self.pStruct:
                return 0

            output: float = 0
            for pId in self.pStruct[id]:
                key: str = ConnGene.genKey(pId, id)
                conn: ConnGene = self.conns[key]
                output += self.evalRec(pId, outputList) * conn.weight + self.nodes[id].bias

            outputList[id] = max(0, output)
            return output

    # ===== MUTATION =====
    def mutate(self, config: dict[str, bool], innovMap: dict[str, int]) -> Genome:
        genome: Genome = deepcopy(self)

        # add new node
        if config["addNode"]:
            fL: int = randint(0, genome.layerNum - 2)
            bL: int = randint(fL + 1, genome.layerNum - 1)
            nId: int = genome.addNode(
                {
                    "inId": (f := choice(genome.layers[fL])),
                    "outId": (b := choice(genome.layers[bL])),
                }
            )

            # set innovation numbers for new connections
            inInnovKey: str = Genome.genInnovKey(genome.lMap[f], genome.lMap[nId], f, nId)
            inInnov: int
            if inInnovKey not in innovMap:
                inInnov = innovMap["SIZE"]

                innovMap[inInnovKey] = inInnov
                innovMap["SIZE"] += 1
            else:
                inInnov = innovMap[inInnovKey]

            genome.conns[ConnGene.genKey(f, nId)].innov = inInnov

            outInnovKey: str = Genome.genInnovKey(genome.lMap[nId], genome.lMap[b], nId, b)
            outInnov: int
            if outInnovKey not in innovMap:
                outInnov = innovMap["SIZE"]

                innovMap[outInnovKey] = outInnov
                innovMap["SIZE"] += 1
            else:
                outInnov = innovMap[outInnovKey]

            genome.conns[ConnGene.genKey(nId, b)].innov = outInnov

        # add new connection
        if config["addConn"]:
            fL: int = randint(0, genome.layerNum - 2)
            bL: int = randint(fL + 1, genome.layerNum - 1)
            f: int = choice(genome.layers[fL])
            b: int = choice(genome.layers[bL])

            # get innovation number
            innovKey: str = Genome.genInnovKey(genome.lMap[f], genome.lMap[b], f, b)
            innov: int
            if innovKey not in innovMap:
                innov = innovMap["SIZE"]

                innovMap[innovKey] = innov
                innovMap["SIZE"] += 1
            else:
                innov = innovMap[innovKey]

            genome.addConn({"inId": f, "outId": b, "innov": innov})

        # mutate bias
        if config["mutBias"]:
            genome.nodes[choice(list(genome.nodes.keys()))].setBias(random())

        # mutate weight
        if config["mutWeight"]:
            genome.conns[choice(list(genome.conns.keys()))].setWeight(random())

        # mutate connection
        if config["mutConn"]:
            genome.conns[choice(list(genome.conns.keys()))].setEnabled(random() > 0.5)

        return genome

    # == topological based mutation methods ==
    # add node
    def addNode(self, config: dict[str, object]) -> int:
        id: int = len(self.nodes)

        # create new node
        self.nodes[id] = NodeGene({"id": id, "type": NodeType.HIDDEN, "bias": 0})

        # create weight for OG inNode to the new node
        w: float
        ogKey: str = ConnGene.genKey(config["inId"], config["outId"])
        if ogKey in self.conns:
            ogConn: ConnGene = self.conns[ogKey]
            # disable original connection
            ogConn.setEnabled(False)
            # get original weight
            w = ogConn.weight

        # if no connection between nodes, set random weight
        else:
            w = uniform(-1, 1)

        # add connections
        self.addConn({"inId": config["inId"], "outId": id, "weight": w, "innov": -1})
        self.addConn({"inId": id, "outId": config["outId"], "weight": 1, "innov": -1})

        return id

    # add connection
    def addConn(self, config: dict[str, object]) -> None:
        # randomly generate weight if not given
        if "weight" not in config:
            config["weight"] = uniform(-1, 1)

        # create and add connection
        conn: ConnGene = ConnGene(config)
        self.conns[conn.key] = conn

        # maintain topological structure data
        # child structure dict
        if config["inId"] not in self.cStruct:
            self.cStruct[config["inId"]] = []

        if config["outId"] not in self.cStruct[config["inId"]]:
            self.cStruct[config["inId"]].append(config["outId"])

        # parent structure dict
        if config["outId"] not in self.pStruct:
            self.pStruct[config["outId"]] = []

        if config["inId"] not in self.pStruct[config["outId"]]:
            self.pStruct[config["outId"]].append(config["inId"])

        # layer map and layer dict
        toUpdate: List[int] = [config["outId"]]
        while len(toUpdate) > 0:
            head: int = toUpdate.pop(0)

            # remove head from old layer list
            oldLayer: int = -1
            newLayer: int = max(map(lambda pid: self.lMap[pid], self.pStruct[head])) + 1

            if head in self.lMap:
                oldLayer = self.lMap[head]

                if oldLayer == newLayer:
                    continue

                if head in self.layers[oldLayer]:
                    self.layers[oldLayer].remove(head)

            # update layer map
            self.lMap[head] = newLayer

            # add head to layer list
            if newLayer not in self.layers:
                self.layers[newLayer] = []
            self.layers[newLayer].append(head)

            # if head has children, update children
            if head in self.cStruct:
                for child in self.cStruct[head]:
                    # add child to queue
                    if child not in toUpdate:
                        toUpdate.append(child)

        # update layer count
        self.layerNum = len(self.layers)

    # == value based mutation methods ==
    # enabled/disabled connection
    def toggleConn(self, config: dict[str, object]) -> None:
        key: str
        if "key" not in config:
            key = ConnGene.genKey(config["inId"], config["outId"])
        else:
            key = config["key"]

        self.conns[key].setEnabled(config["enabled"])

    # update weight of connection
    def setWeight(self, config: dict[str, object]) -> None:
        key: str
        if "key" not in config:
            key = ConnGene.genKey(config["inId"], config["outId"])
        else:
            key = config["key"]

        self.conns[key].setWeight(config["weight"])

    # update bias of node
    def setBias(self, config: dict[str, object]) -> None:
        self.nodes[config["id"]].setBias(config["bias"])

    # generate innovation key
    def genInnovKey(fL: int, bL: int, f: int, b: int) -> str:
        return "{}.{}-{}.{}".format(fL, bL, f, b)

    # ===== DEBUG / PRINTERS ======
    # custom string representation
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        rt: str = ""

        nL: int = len(self.nodes) - 1
        for i, (_, v) in enumerate(self.nodes.items()):
            if i == 0:
                b = "╔═ "
            elif i == nL:
                b = "\n╠═ "
            else:
                b = "\n║  "

            rt += b + str(v)

        cL: int = len(self.conns) - 1
        for i, (_, v) in enumerate(self.conns.items()):
            if i == 0 and cL != 0:
                b = "\n╠═ "
            elif i == cL:
                b = "\n╚═ "
            else:
                b = "\n║  "

            rt += b + str(v)

        return rt
