from math import isnan
from typing import Tuple
import sys, getopt

from data.data import AGENT_CLASS_TYPE, REP
from scripts.auto import App as Auto
from scripts.average import App as Average
from scripts.play import App as Play


# parse console arguments
def parseOptions(opts, args) -> Tuple[type, dict[str, object], int]:
    app: type = None
    p: int = AGENT_CLASS_TYPE.CTRL
    g1: int = AGENT_CLASS_TYPE.OGNL
    g2: int = AGENT_CLASS_TYPE.RAND
    itr: int = 1

    for opt, arg in opts:
        # print help text and terminate
        if opt == "h":
            printHelp()
            sys.exit()

        # set app file
        elif opt in ("-a", "--app"):
            if arg in ("0", "play"):
                app = Play
            elif arg in ("1", "auto"):
                app = Auto
                p = AGENT_CLASS_TYPE.RAND
            elif arg in ("2", "average"):
                app = Average
                p = AGENT_CLASS_TYPE.RAND
            else:
                printHelp()
                sys.exit(2)

        # set first ghost type
        elif opt in ("-f", "--ghostF"):
            if arg in ("2", "aggressive"):
                g1 = AGENT_CLASS_TYPE.AGGR
            elif arg in ("3", "mdp"):
                g1 = AGENT_CLASS_TYPE.SMDP
            elif arg in ("4", "td"):
                g1 = AGENT_CLASS_TYPE.GDQL
            elif arg in ("5", "ne"):
                g1 = AGENT_CLASS_TYPE.NEAT

        # set second ghost type
        elif opt in ("-s", "--ghostS"):
            if arg in ("2", "aggressive"):
                g2 = AGENT_CLASS_TYPE.AGGR
            elif arg in ("3", "mdp"):
                g2 = AGENT_CLASS_TYPE.SMDP
            elif arg in ("4", "td"):
                g2 = AGENT_CLASS_TYPE.GDQL
            elif arg in ("5", "ne"):
                g2 = AGENT_CLASS_TYPE.NEAT

        # set iterations
        elif opt in ("-i", "--iterations"):
            itr = int(arg)
            if isnan(itr):
                print("Iteration count not a valid number")
                sys.exit(2)

    secondary = g2
    if g2 == AGENT_CLASS_TYPE.SMDP or g2 == AGENT_CLASS_TYPE.GDQL or g2 == AGENT_CLASS_TYPE.NEAT:
        secondary = {
            REP.INKY: AGENT_CLASS_TYPE.NONE,
            REP.CLYDE: AGENT_CLASS_TYPE.NONE,
            REP.PINKY: g2,
        }

    return app, {REP.PACMAN: p, REP.BLINKY: g1, "secondary": secondary}, itr

# print help text
def printHelp() -> None:
    print("launch.py -a <app name> -f <first ghost variant> -s <secont ghost variant> -i <iterations>")

    print("\n-a --app <app name> options: (required)")
    print("\tplay [player control app]")
    print("\tauto [baseline agent app]")
    print("\taverage [average performance app w/o gui]")

    print("\n-f --ghostF <first ghost variant> options: (optional, default = 1)")
    print("\t1 [variant 1 - original]")
    print("\t2 [variant 2 - hyperaggressive]")
    print("\t3 [variant 3 - mdp based]")
    print("\t4 [variant 4 - td learning based]")
    print("\t5 [variant 5 - neuroevolutionary based]\n")

    print("\n-s --ghostS <second ghost variant> options: (optional, default = \"random\")")
    print("\t2 [variant 2 - hyperaggressive]")
    print("\t3 [variant 3 - mdp based]")
    print("\t4 [variant 4 - td learning based]")
    print("\t5 [variant 5 - neuroevolutionary based]")
    print("\trandom [random original variant - inky, clyde, or pinky]\n")

    print("\n-i --iterations (optional, default = 1)")
    print("\t<any integer value>")


class Launcher:
    def __init__(self, app: type, config: dict[str, object]) -> None:
        self.config = config
        self.app = app

    # run app
    def run(self) -> None:
        self.app(self.config).start()


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:f:s:i:", ["app=", "ghostF=", "ghostS=", "iterations="])
    except:
        printHelp()
        sys.exit(2)

    if len(opts) < 1:
        printHelp()
        sys.exit(2)

    # parse options
    app, agents, iterations = parseOptions(opts, args)

    # create base config
    baseConfig: dict[str, object] = {
        "enablePwrPlt": True,
        "gameSpeed": 0.2,
        "genomes": {
            REP.BLINKY: ("saves", "ghost", 33),
            REP.PINKY: ("saves", "ghost", 33),
        },
        "neuralnets": {
            REP.PACMAN: ("saves", "pacman", 63),
            REP.BLINKY: ("saves", "ghost", 35),
            REP.PINKY: ("saves", "ghost", 35),
        }
    }

    # add iteration data
    baseConfig["iterations"] = iterations

    # add agent data
    baseConfig["agents"] = agents

    # create launcher and execute
    launcher: Launcher = Launcher(app, baseConfig)
    launcher.run()
