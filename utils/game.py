from agents.base import GhostAgent
from agents.blinky import BlinkyClassicAgent, BlinkyClassicAggrAgent
from agents.clyde import ClydeClassicAgent, ClydeClassicAggrAgent
from agents.inky import InkyClassicAgent, InkyClassicAggrAgent
from agents.pinky import PinkyClassicAgent, PinkyClassicAggrAgent
from agents.pacman import PacmanDQLAgent
from data.data import GHOST_CLASS_TYPE
from game.game import Game
from utils.file import loadNeuralNetT


def newGame(ghosts: dict[str, int], enablePwrPlt: bool, neuralnets: dict[str, str], genomes: dict[str, str]) -> Game:
    # create ai pacman agent
    pacman: PacmanDQLAgent = PacmanDQLAgent(loadNeuralNetT(neuralnets["pacman"]))

    # create ai blinky agent
    blinky: GhostAgent = None
    if ghosts["blinky"] == GHOST_CLASS_TYPE.OGNL:
        blinky = BlinkyClassicAgent()
    elif ghosts["blinky"] == GHOST_CLASS_TYPE.AGGR:
        blinky = BlinkyClassicAggrAgent()

    # create ai inky agent
    inky: GhostAgent = None
    if ghosts["inky"] == GHOST_CLASS_TYPE.OGNL:
        inky = InkyClassicAgent()
    elif ghosts["inky"] == GHOST_CLASS_TYPE.AGGR:
        inky = InkyClassicAggrAgent()

    # create ai clyde agent
    clyde: GhostAgent = None
    if ghosts["clyde"] == GHOST_CLASS_TYPE.OGNL:
        clyde = ClydeClassicAgent()
    elif ghosts["clyde"] == GHOST_CLASS_TYPE.AGGR:
        clyde = ClydeClassicAggrAgent()

    # create ai pinky agent
    pinky: GhostAgent = None
    if ghosts["pinky"] == GHOST_CLASS_TYPE.OGNL:
        pinky = PinkyClassicAgent()
    elif ghosts["pinky"] == GHOST_CLASS_TYPE.AGGR:
        pinky = PinkyClassicAggrAgent()

    return Game(pacman, blinky, inky, clyde, pinky, enablePwrPlt)
