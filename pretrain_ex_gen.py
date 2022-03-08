from tkinter import Tk
import _thread

from agents.pacman import PacmanMDPAgent, pacmanFeatureExtraction
from agents.blinky import BlinkyClassicAgent
from agents.pinky import PinkyClassicAgent
from game.game import Game
from gui.display import Display
from utils.printer import printPacmanPerfomance


class MDPGuidedTraining:
    def __init__(self, config: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("MDP Guided Training")

            self.display: Display = Display(self.main)

        # reward constants
        self.rewards: dict[str, float] = config["rewards"]

        # mdp config
        self.mdpConfig: float = config["mdpConfig"]

        # training config
        self.gameCap: int = config["gameCap"]

    # start training (main function)
    def start(self) -> None:
        # start display
        if self.hasDisplay:
            _thread.start_new_thread(self.training, ())
            self.main.mainloop()

        else:
            self.training()

    def newGame(self) -> Game:
        return Game(
            PacmanMDPAgent(self.rewards, self.mdpConfig),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent(),
        )

    # ===== main training function =====
    def training(self) -> None:
        eps: int = 0

        # create new game
        game: Game = self.newGame()
        if self.hasDisplay:
            self.display.newGame(game)

        # create new save file for new run
        # open("./out/DG_DQL_EX/run{}.txt".format(ep), "x")

        while True:
            # save array
            # runFile = open("./out/DG_DQL_EX/run{}.txt".format(ep), "a")
            # runFile.write(str(features) + "\n")
            # runFile.close()

            # perform next step
            gameover, won, atePellet, atePwrPlt, ateGhost = game.nextStep()

            # rerender display if enabled
            if self.hasDisplay:
                self.display.rerender()

            # reset game when gameover
            if gameover or won:
                printPacmanPerfomance(eps, game)

                # exit loop
                eps += 1
                if eps >= self.gameCap:
                    break

                # create new game
                game = self.newGame()
                if self.hasDisplay:
                    self.display.newGame(game)

                # create new save file for new run
                # open("./out/DG_DQL_EX/run{}.txt".format(ep), "x")


if __name__ == "__main__":
    training: MDPGuidedTraining = MDPGuidedTraining(
        {
            "gameCap": 10,
            "mdpConfig": {
                "maxIter": 10000,
                "gamma": 0.90,
                "epsilon": 0.00005,
            },
            "rewards": {
                "timestep": -0.05,
                "pellet": 5,
                "pwrplt": 2,
                "ghost": -100,
                "kill": 30,
            },
        },
        True,
    )
    training.start()
