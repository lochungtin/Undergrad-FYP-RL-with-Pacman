import numpy as np
from agents.base import GhostAgent
from agents.blinky import BlinkyClassicAgent, BlinkyClassicAggrAgent, BlinkyDQLAgent
from agents.clyde import ClydeClassicAgent, ClydeClassicAggrAgent
from agents.inky import InkyClassicAgent, InkyClassicAggrAgent
from agents.pinky import PinkyClassicAgent, PinkyClassicAggrAgent
from agents.pacman import PacmanDQLAgent
from data.data import GHOST_CLASS_TYPE, REP
from game.game import Game
from utils.file import loadNeuralNetT

# create game with any configuration of agents
def newGame(ghosts: dict[str, int], enablePwrPlt: bool, neuralnets: dict[str, str], genomes: dict[str, str]) -> Game:
    # create ai pacman agent
    pacman: PacmanDQLAgent = PacmanDQLAgent(loadNeuralNetT(neuralnets["pacman"]))

    # create ai blinky agent
    blinky: GhostAgent = None
    if ghosts[REP.BLINKY] == GHOST_CLASS_TYPE.OGNL:
        blinky = BlinkyClassicAgent()
    elif ghosts[REP.BLINKY] == GHOST_CLASS_TYPE.AGGR:
        blinky = BlinkyClassicAggrAgent()
    elif ghosts[REP.BLINKY] == GHOST_CLASS_TYPE.GDQL:
        blinky = BlinkyDQLAgent(loadNeuralNetT(neuralnets[REP.BLINKY]))

    # create ai inky agent
    inky: GhostAgent = None
    if ghosts[REP.INKY] == GHOST_CLASS_TYPE.OGNL:
        inky = InkyClassicAgent()
    elif ghosts[REP.INKY] == GHOST_CLASS_TYPE.AGGR:
        inky = InkyClassicAggrAgent()

    # create ai clyde agent
    clyde: GhostAgent = None
    if ghosts[REP.CLYDE] == GHOST_CLASS_TYPE.OGNL:
        clyde = ClydeClassicAgent()
    elif ghosts[REP.CLYDE] == GHOST_CLASS_TYPE.AGGR:
        clyde = ClydeClassicAggrAgent()

    # create ai pinky agent
    pinky: GhostAgent = None
    if ghosts[REP.PINKY] == GHOST_CLASS_TYPE.OGNL:
        pinky = PinkyClassicAgent()
    elif ghosts[REP.PINKY] == GHOST_CLASS_TYPE.AGGR:
        pinky = PinkyClassicAggrAgent()

    return Game(pacman, blinky, inky, clyde, pinky, enablePwrPlt)


# create game with random g2s (secondary ghost) [Classic Algorithm]
def newRndORGLGhostGame(enablePwrPlt: bool, neuralnets: dict[str, str]) -> Game:
    # create ai pacman agent
    pacman: PacmanDQLAgent = PacmanDQLAgent(loadNeuralNetT(neuralnets["pacman"]))

    inky, clyde, pinky = None, None, None

    # create agent randomly
    selection: int = np.random.randint(0, 3)

    # create agents
    if selection == 0:
        inky = InkyClassicAgent()
    elif selection == 1:
        clyde = ClydeClassicAgent()
    else:
        pinky = PinkyClassicAgent()

    return Game(pacman, BlinkyClassicAgent(), inky, clyde, pinky, enablePwrPlt)


# create game with random g2s (secondary ghost) [Aggressive Classic Algorithm]
def newRndAGGRGhostGame(enablePwrPlt: bool, neuralnets: dict[str, str]) -> Game:
    # create ai pacman agent
    pacman: PacmanDQLAgent = PacmanDQLAgent(loadNeuralNetT(neuralnets["pacman"]))

    inky, clyde, pinky = None, None, None

    # create agent randomly
    selection: int = np.random.randint(0, 3)

    # create agents
    if selection == 0:
        inky = InkyClassicAggrAgent()
    elif selection == 1:
        clyde = ClydeClassicAggrAgent()
    else:
        pinky = PinkyClassicAggrAgent()

    return Game(pacman, BlinkyClassicAggrAgent(), inky, clyde, pinky, enablePwrPlt)