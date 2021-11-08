from random import random

from gene import Gene
from genome import Genome


class Utils:
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
