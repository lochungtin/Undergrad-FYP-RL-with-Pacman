from data.data import GHOST_CLASS_TYPE
from game.game import Game
from utils.game import newGame, newRndAGGRGhostGame, newRndORGLGhostGame
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # game config
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
        game: Game = newRndAGGRGhostGame(self.enablePwrPlt, self.neuralnets)

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
            "iterations": 1000,
            "neuralnets": {"pacman": ("out", "RL0803_1832", 9895)},
        }
    )
    app.start()
