from typing import Tuple
from data.data import AGENT_CLASS_TYPE, REP
from game.game import Game, newGame
from utils.printer import printPacmanPerfomance


class App:
    def __init__(self, config: dict[str, object]) -> None:
        # agent config
        self.agents: dict[str, object] = config["agents"]

        # game config
        self.enablePwrPlt: bool = config["enablePwrPlt"]

        # neural net config files
        self.neuralnets: dict[str, str] = config["neuralnets"]

        # genomes config files
        self.genomes: dict[str, str] = config["genomes"]

        # iterations
        self.iterations: int = config["iterations"]

    # start average run
    def start(self, verbose: bool = False) -> Tuple[float, int, int]:
        avgC: float = 0
        avgT: float = 0
        avgD: float = 0

        for i in range(self.iterations):
            completion, timesteps, deathCount = self.runGame(i)

            avgC += completion
            avgT += timesteps
            avgD += deathCount


        avgC /= self.iterations
        avgT /= self.iterations
        avgD /= self.iterations

        if verbose:
            print("Average Completion Rate: {}\nAverage Timesteps: {}\nAverage Death Count: {}".format(avgC, avgT, avgD))

        return avgC, avgT, avgD

    # run game
    def runGame(self, iteration: int) -> Tuple[float, int, int]:
        game: Game = newGame(self.agents, self.enablePwrPlt, self.neuralnets, self.genomes)

        ghostDeathCount: int = 0
        while True:
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            ghostDeathCount += ateGhost * 1

            if gameover or won or game.timesteps > 200:
                break

        return printPacmanPerfomance(iteration, game, True), game.timesteps, ghostDeathCount


if __name__ == "__main__":
    app: App = App(
        {
            "agents": {
                REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                REP.BLINKY: AGENT_CLASS_TYPE.GDQL,
                "secondary": AGENT_CLASS_TYPE.RAND,
            },
            "enablePwrPlt": True,
            "genomes": {
                REP.BLINKY: ("saves", "ghost", 33),
                REP.PINKY: ("saves", "ghost", 33),
            },
            "iterations": 1000,
            "neuralnets": {
                REP.PACMAN: ("saves", "pacman", 63),
                REP.BLINKY: ("saves", "ghost", 35),
                REP.PINKY: ("saves", "ghost", 35),
            },
        }
    )
    app.start()
