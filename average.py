from data.data import GHOST_CLASS_TYPE
from game.game import Game
from utils.game import newGame, newRndClassicGhostGame
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # game config
        self.ghosts: dict[str, int] = config["ghosts"]
        self.enablePwrPlt: bool = config["enablePwrPlt"]

        # neural net
        self.neuralnets: dict[str, str] = config["neuralnets"]

        # genomes
        self.genomes: dict[str, str] = config["genomes"]

        # iterations
        self.iterations: int = config["iterations"]

    def start(self) -> None:
        average: float = 0

        for i in range(self.iterations):
            average += self.runGame()

        print("Average Completion Rate: {}".format(average / self.iterations))

    def runGame(self) -> float:
        game: Game = newRndClassicGhostGame(self.enablePwrPlt, self.neuralnets)

        while True:
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()
            if gameover or won or game.timesteps > 1000:
                break                

        return printPacmanPerfomance(0, game, True)


if __name__ == "__main__":
    app: App = App(
        {
            "enablePwrPlt": True,
            "genomes": {},
            "ghosts": {
                "blinky": GHOST_CLASS_TYPE.OGNL,
                "inky": GHOST_CLASS_TYPE.NONE,
                "clyde": GHOST_CLASS_TYPE.NONE,
                "pinky": GHOST_CLASS_TYPE.OGNL,
            },
            "iterations": 1000,
            "neuralnets": {"pacman": ("out", "RL0803_1832", 9895)},
        }
    )
    app.start()
