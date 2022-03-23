from datetime import datetime
import os
from typing import List, Tuple

from average import App
from data.data import AGENT_CLASS_TYPE, REP


class Experiment:
    def __init__(self, combinations: List[Tuple[str, dict[str, object]]]) -> None:
        self.combinations = combinations

    def createConfig(self, agents: dict[str, object]) -> dict[str, object]:
        return {
            "agents": agents,
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

    def runPass(self, config: dict[str, object]) -> float:
        return App(config).start(True)

    def start(self) -> None:
        filename: str = "./log/EXP{}.txt".format(datetime.now().strftime("%d%m_%H%M"))
        open(filename, "x")

        for set in self.combinations:
            label: str = set[0]
            agents: dict[str, object] = set[1]

            average: float = self.runPass(self.createConfig(agents))

            logFile = open(filename, "a")
            logFile.write("{}: {}\n".format(label, average))
            logFile.close()


if __name__ == "__main__":
    experiment: Experiment = Experiment(
        [
            # control run
            # original implementation
            (
                "CTRL OGNL (OGNL / OGNL) [    VAR1    ]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.OGNL,
                    "secondary": AGENT_CLASS_TYPE.RAND,
                    "randType": AGENT_CLASS_TYPE.OGNL,
                },
            ),
            # experiment 1:
            # full aggressive
            (
                "EXP1 AGGR (AGGR / AGGR) [    VAR2    ]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.AGGR,
                    "secondary": AGENT_CLASS_TYPE.RAND,
                    "randType": AGENT_CLASS_TYPE.AGGR,
                },
            ),
            # experiment 2:
            # single ghost modification - one variant / one original
            (
                "EXP2 SMOD (AGGR / OGNL) [VAR2 -- VAR1]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.AGGR,
                    "secondary": AGENT_CLASS_TYPE.RAND,
                    "randType": AGENT_CLASS_TYPE.OGNL,
                },
            ),
            (
                "EXP2 SMOD (SMDP / OGNL) [VAR3 -- VAR1]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.SMDP,
                    "secondary": AGENT_CLASS_TYPE.RAND,
                    "randType": AGENT_CLASS_TYPE.OGNL,
                },
            ),
            (
                "EXP2 SMOD (GDQL / OGNL) [VAR4 -- VAR1]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.GDQL,
                    "secondary": AGENT_CLASS_TYPE.RAND,
                    "randType": AGENT_CLASS_TYPE.OGNL,
                },
            ),
            (
                "EXP2 SMOD (NEAT / OGNL) [VAR5 -- VAR1]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.NEAT,
                    "secondary": AGENT_CLASS_TYPE.RAND,
                    "randType": AGENT_CLASS_TYPE.OGNL,
                },
            ),
            # experiment 3:
            # double ghost modification
            (
                "EXP3 DMOD (AGGR / SMDP) [VAR2 -- VAR3]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.AGGR,
                    "secondary": {
                        REP.INKY: AGENT_CLASS_TYPE.NONE,
                        REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                        REP.PINKY: AGENT_CLASS_TYPE.SMDP,
                    },
                },
            ),
            (
                "EXP3 DMOD (AGGR / GDQL) [VAR2 -- VAR4]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.AGGR,
                    "secondary": {
                        REP.INKY: AGENT_CLASS_TYPE.NONE,
                        REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                        REP.PINKY: AGENT_CLASS_TYPE.GDQL,
                    },
                },
            ),
            (
                "EXP3 DMOD (AGGR / NEAT) [VAR2 -- VAR5]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.AGGR,
                    "secondary": {
                        REP.INKY: AGENT_CLASS_TYPE.NONE,
                        REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                        REP.PINKY: AGENT_CLASS_TYPE.NEAT,
                    },
                },
            ),
            (
                "EXP3 DMOD (SMDP / GDQL) [VAR3 -- VAR4]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.SMDP,
                    "secondary": {
                        REP.INKY: AGENT_CLASS_TYPE.NONE,
                        REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                        REP.PINKY: AGENT_CLASS_TYPE.GDQL,
                    },
                },
            ),
            (
                "EXP3 DMOD (SMDP / NEAT) [VAR3 -- VAR5]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.SMDP,
                    "secondary": {
                        REP.INKY: AGENT_CLASS_TYPE.NONE,
                        REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                        REP.PINKY: AGENT_CLASS_TYPE.NEAT,
                    },
                },
            ),
            (
                "EXP3 DMOD (GDQL / NEAT) [VAR4 -- VAR5]",
                {
                    REP.PACMAN: AGENT_CLASS_TYPE.RAND,
                    REP.BLINKY: AGENT_CLASS_TYPE.GDQL,
                    "secondary": {
                        REP.INKY: AGENT_CLASS_TYPE.NONE,
                        REP.CLYDE: AGENT_CLASS_TYPE.NONE,
                        REP.PINKY: AGENT_CLASS_TYPE.NEAT,
                    },
                },
            ),
        ]
    )
    experiment.start()
