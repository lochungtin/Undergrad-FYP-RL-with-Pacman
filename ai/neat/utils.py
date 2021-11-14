from random import random
from datetime import datetime
import json
from typing import List

from ai.neat.gene import Gene
from ai.neat.genome import Genome


class Utils:
    # reproduce offspring
    def reproduce(p1: Genome, p2: Genome) -> Genome:
        offspring: Genome = Genome(p1.inNo, p1.outNo)

        loopSize: int = p1.maxInnov
        if p2.maxInnov > p1.maxInnov:
            loopSize = p2.maxInnov

        if p1.fitness == p2.fitness:
            for innov in range(1, loopSize + 1):
                p1G: Gene = p1.getGene(innov)
                p2G: Gene = p2.getGene(innov)

                if p1G == None and p2G != None:
                    offspring.addGene(p2G)
                elif p2G == None and p1G != None:
                    offspring.addGene(p1G)
                elif p1G != None and p2G != None:
                    if random() > 0.5:
                        offspring.addGene(p2G)
                    else:
                        offspring.addGene(p1G)

            return offspring

        dom: Genome = p1
        rec: Genome = p2
        if p1.fitness < p2.fitness:
            dom = p2
            rec = p1

        for innov in range(1, loopSize + 1):
            dG: Gene = dom.getGene(innov)
            rG: Gene = rec.getGene(innov)

            if dG != None and rG == None:
                offspring.addGene(dG)
            elif dG != None and rG != None:
                if random() > 0.5:
                    offspring.addGene(dG)
                else:
                    offspring.addGene(rG)

        return offspring

    # calculate compatibility distance
    def getCompDist(g1: Genome, g2: Genome, cE: float, cD: float, cW: float) -> float:
        N: int = g1.maxInnov
        E: int = N - g2.maxInnov
        if g2.maxInnov > g1.maxInnov:
            N = g2.maxInnov
            E = N - g1.maxInnov

        D: int = 0
        W: float = 0
        for innov in range(1, N - E + 1):
            g1G: Gene = g1.getGene(innov)
            g2G: Gene = g2.getGene(innov)

            if g1G == None and g2G != None:
                D += 1
                W += g2G.weight
            elif g2G == None and g1G != None:
                D += 1
                W += g1G.weight
            elif g1G != None and g2G != None:
                W += abs(g1G.weight - g2G.weight)

        W /= N

        if N < 20:
            N = 1

        return (cE * E / N) + (cD * D / N) + (cW * W)

    # calculate adjusted fitness against the population
    def adjFitness(
        g: Genome, pop: List[Genome], cE: float, cD: float, cW: float, dThres: float
    ):
        adjustment: int = 0
        for genome in pop:
            adjustment += (Utils.getCompDist(g, genome, cE, cD, cW) <= dThres) * 1

        g.fitness /= adjustment
        return g.fitness

    # save genome data
    def save(genome: Genome, generation: int, prefix: str = "") -> None:
        result: dict[str, object] = {}
        genes: dict[int, dict[str, float]] = {}

        result["inNo"] = genome.inNo
        result["outNo"] = genome.outNo
        result["maxInnov"] = genome.maxInnov

        for _, (_, gene) in enumerate(genome.genes.items()):
            data: dict[str, float] = {}

            data["inNode"] = gene.inNode
            data["outNode"] = gene.outNode
            data["weight"] = gene.weight
            data["enabled"] = gene.enabled * 1
            data["innov"] = gene.innov

            genes[gene.innov] = data

        result["genes"] = genes

        filename: str = "./out/{}-gen{}-{}.json".format(
            prefix, generation, datetime.now().strftime("%d:%m:%Y:%H:%M:%S")
        )
        with open(filename, "w") as outfile:
            json.dump(result, outfile)

    # create genome from data
    def load(filename: str) -> Genome:
        result: Genome = None
        with open(filename) as infile:
            data: dict[str, object] = json.load(infile)

            result: Genome = Genome(data["inNo"], data["outNo"])
            result.maxInnov = data["maxInnov"]

            for _, (_, geneData) in enumerate(data["genes"].items()):
                result.addGene(
                    Gene(
                        geneData["inNode"],
                        geneData["outNode"],
                        geneData["weight"],
                        geneData["enabled"] == 1,
                        geneData["innov"],
                    )
                )

        return result
