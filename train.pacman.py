from neat.genome import Genome
from neat.utils import Utils


def main():

    g = Genome(4, 2)
    g.baseInit()

    print(g)

    Utils.save(g, 1, "pacman-neat")

    pass


if __name__ == "__main__":
    main()
