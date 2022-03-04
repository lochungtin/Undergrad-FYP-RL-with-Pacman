from tkinter import Tk
import _thread

from agents.pacman import PacmanMDPAgent, pacmanFeatureExtraction
from agents.blinky import BlinkyClassicAgent
from agents.pinky import PinkyClassicAgent
from game.game import Game
from gui.display import Display


class MDPGuidedTraining:
    def __init__(self, trainingConfig: dict[str, object], hasDisplay: bool = False) -> None:
        # display
        self.hasDisplay: bool = hasDisplay
        if hasDisplay:
            self.main: Tk = Tk()
            self.main.title("MDP Guided Training")

            self.display: Display = Display(self.main)

        # mdp config
        self.gamma: float = trainingConfig["mdpConfig"]["gamma"]
        self.epsilon: float = trainingConfig["mdpConfig"]["epsilon"]

        self.maxIter: int = trainingConfig["mdpConfig"]["maxIterations"]

        # reward constants
        self.rewards: dict[str, float] = trainingConfig["rewards"]

        # training config
        self.gameCap: int = trainingConfig["gameCap"]

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
            PacmanMDPAgent(self.rewards, self.gamma, self.epsilon, self.maxIter),
            blinky=BlinkyClassicAgent(),
            pinky=PinkyClassicAgent(),
        )

    # ===== main training function =====
    def training(self) -> None:
        ep: int = 0

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
                self.printPerformance(ep, game)

                # exit loop
                ep += 1
                if ep >= self.gameCap:
                    break

                # create new game
                game = self.newGame()
                if self.hasDisplay:
                    self.display.newGame(game)

                # create new save file for new run
                # open("./out/DG_DQL_EX/run{}.txt".format(ep), "x")

    def printPerformance(self, ep: int, game: Game) -> None:
        consumption: int = 68 - game.pelletProgress
        print(
            "ep: {}\tt: {}\tl: {}\tc: {}/68 = {}%".format(
                ep,
                game.timesteps,
                game.pelletProgress,
                consumption,
                round(consumption / 68 * 100, 2),
            )
        )


if __name__ == "__main__":
    training: MDPGuidedTraining = MDPGuidedTraining(
        {
            "gameCap": 10,
            "mdpConfig": {
                "maxIterations": 10000,
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
        False,
    )
    training.start()
