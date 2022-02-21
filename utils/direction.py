from typing import List


class DIR:
    UP = 0
    DW = 1
    LF = 2
    RT = 3

    def getList() -> List[int]:
        return [DIR.UP, DIR.DW, DIR.LF, DIR.RT]

    def opposite(dir) -> int:
        if dir == DIR.UP:
            return DIR.DW
        if dir == DIR.DW:
            return DIR.UP
        if dir == DIR.LF:
            return DIR.RT
        return DIR.LF
