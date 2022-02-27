import json
from typing import List, Tuple


# load examples from file
def loadFile(ep: int) -> List[Tuple[List[float], List[int]]]:
    rt: List[Tuple[List[float], List[int]]] = []

    with open("./out/DG_DQL_EX/run{}.txt".format(ep), "r") as file:
        for line in file:
            dataArr: List[float] = json.loads(line)
            dLength: int = len(dataArr) - 1

            # parse data array
            featureVec: List[float] = dataArr[0: dLength]

            actionVal: List[int] = [0, 0, 0, 0]
            actionVal[dataArr[dLength]] = 1

            rt.append((featureVec, actionVal))

    return rt


def main():
    print(loadFile(1))


if __name__ == "__main__":
    main()
