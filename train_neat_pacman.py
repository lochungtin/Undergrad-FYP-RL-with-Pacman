from ai.neat.genome import Genome
from ai.neat.utils import Utils
from game.paiv import PAIV


cT: float = 0
cP: float = 0
cW: float = 0
cL: float = 0


def runSim(genome: Genome, enableGhost: bool, enablePwrPlt) -> float:
    game: PAIV = PAIV(genome, enableGhost, enablePwrPlt)

    pelletCount: int = 0
    gameover: bool = False
    won: bool = False
    while game.pelletDrought < 50 and not gameover and not won:
        gameover, won, atePellet = game.nextStep()

        if atePellet:
            pelletCount += 0

    genome.fitness = cT * game.timesteps + cP * pelletCount + cW * won + cL * gameover

    return genome.fitness


if __name__ == "__main__":
    pass
