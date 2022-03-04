from typing import List


dirList: List[int] = [0, 1, 2, 3]

class DIR:
    UP = 0
    DW = 1
    LF = 2
    RT = 3

    def getList() -> List[int]:
        return dirList

    def getOpposite(dir) -> int:
        if dir == DIR.UP:
            return DIR.DW
        if dir == DIR.DW:
            return DIR.UP
        if dir == DIR.LF:
            return DIR.RT
        return DIR.LF
