from copy import deepcopy
from random import random
from datetime import datetime
from typing import List
import json

from ai.neat.gene import ConnGene, NodeGene
from ai.neat.genome import Genome


class GenomeUtils:
    CROSS_OPTIONS = {
        "MIN": 0,
        "MAX": 1,
        "RAN": 2,
    }

    # ===== fitness related =====
    # get compatibility distance
    def getCompDist(g1: Genome, g2: Genome, conf: dict[str, float]):
        genes: dict[int, ConnGene] = {}
        g1Max, g2Max = 0, 0
        for (key, gene) in g1.conns.items():
            genes[key] = gene.innov
            if gene.innov > g1Max:
                g1Max = gene.innov

        for (key, gene) in g2.conns.items():
            genes[key] = gene.innov
            if gene.innov > g2Max:
                g2Max = gene.innov

        n: int = len(genes)
        e: int = abs(len(g1.conns) - len(g2.conns))
        smaller: int = min(g1Max, g2Max)

        d, m, w = 0, 1, 0

        for (key, innov) in genes.items():
            if innov > smaller:
                break

            if key in g1.conns:
                c1: ConnGene = g1.conns[key]
            else:
                d += 1
                continue

            if key in g2.conns:
                c2: ConnGene = g2.conns[key]
            else:
                d += 1
                continue

            m += 1
            w += abs(c1.weight - c2.weight)

        return (conf["cE"] * e / n) + (conf["cD"] * d / n) + (conf["cW"] * w / m)

    # get down scale factor for fitness
    def fitnessAdj(g: Genome, pop: List[Genome], conf: dict[str, float]) -> float:
        adjustment: int = 0
        for genome in pop:
            adjustment += (
                GenomeUtils.getCompDist(g, genome, conf) <= conf["dThres"]
            ) * 1

        return adjustment

    # ===== crossing related =====
    # reproduce offspring, g1 is fitter
    def cross(g1: Genome, g2: Genome, options: int) -> Genome:
        g: Genome = deepcopy(g1)

        for (key, gene) in g2.conns.items():
            if (
                options == GenomeUtils.CROSS_OPTIONS["MAX"]
                or (
                    options == GenomeUtils.CROSS_OPTIONS["MIN"]
                    and key in g.conns
                    and random() > 0.5
                )
                or (options == GenomeUtils.CROSS_OPTIONS["MAX"] and random() > 0.5)
            ):

                bypass: bool = False

                i, o = ConnGene.parseKey(key)
                if i not in g.nodes:
                    g.nodes[i] = g2.nodes[i]
                    bypass = True

                if o not in g.nodes:
                    g.nodes[o] = g2.nodes[o]
                    bypass = True

                # add connection
                if bypass or g.lMap[o] >= g.lMap[i]:
                    conf: dict[str, object] = {
                        "inId": i,
                        "outId": o,
                        "key": key,
                        "weight": gene.weight,
                        "enabled": gene.enabled,
                        "innov": gene.innov,
                    }
                    g.addConn(conf)

        return g

    # ===== save and load functions =====
    # save genome config
    def save(genome: Genome, runPref: str, generation: int) -> str:
        data: dict[str, object] = {}

        data["inSize"] = genome.inSize
        data["outSize"] = genome.outSize
        data["nodes"] = {}
        for (key, node) in genome.nodes.items():
            data["nodes"][key] = {
                "id": node.id,
                "type": node.type,
                "bias": node.bias,
            }

        data["conns"] = {}
        for (key, conn) in genome.conns.items():
            data["conns"][key] = {
                "key": conn.key,
                "weight": conn.weight,
                "enabled": conn.enabled,
            }

        data["cStruct"] = genome.cStruct
        data["layers"] = genome.layers

        filename: str = "./out/{}/ne-genome-gen{}.json".format(runPref, generation)
        with open(filename, "w+") as outfile:
            json.dump(data, outfile)

        return filename

    # save innovation map data
    def saveInnov(innov: dict[str, int], runPref: str, generation: int) -> str:
        filename: str = "./out/{}/ne-innov-gen{}.json".format(runPref, generation)
        with open(filename, "w+") as outfile:
            json.dump(innov, outfile)

        return filename

    # load genome
    def load(filename: str, plain: bool = False) -> Genome:

        if not filename.startswith("./out"):
            filename = "./out/{}".format(filename)

        genome: Genome = None
        with open(filename, "r") as infile:
            if plain:
                return json.load(infile)

            else:
                data: dict[str, object] = json.load(infile)

                genome: Genome = Genome(data)

                genome.cStruct = {}
                genome.layers = {}
                genome.nodes = {}
                genome.conns = {}
                genome.pStruct = {}
                genome.lMap = {}

                for (key, node) in data["nodes"].items():
                    genome.nodes[int(key)] = NodeGene(node)

                for (key, conn) in data["conns"].items():
                    genome.conns[key] = ConnGene(conn)

                # recreate pStruct from cStruct
                for (p, children) in data["cStruct"].items():
                    genome.cStruct[int(p)] = children
                    for c in children:
                        if c not in genome.pStruct:
                            genome.pStruct[int(c)] = []

                        genome.pStruct[int(c)].append(int(p))

                # recreate lMap from layers
                for (layer, nodes) in data["layers"].items():
                    genome.layers[int(layer)] = nodes
                    for node in nodes:
                        genome.lMap[int(node)] = int(layer)

                # set layer num
                genome.layerNum = len(genome.layers)

                return genome

    # load innovation map
    def loadInnov(filename: str) -> dict[str, int]:
        if not filename.startswith("./out"):
            filename = "./out/{}".format(filename)

        with open(filename, "r") as infile:
            return json.load(infile)
