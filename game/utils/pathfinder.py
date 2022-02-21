from re import search
from typing import List
from queue import Queue
import math

from data.config import BOARD, POS
from data.data import BOARD, REP
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR

class PFDataCell:
    def __init__(self) -> None:
        self.f: float = math.inf
        self.g: float = -1
        self.h: float = -1

        self.parent: CPair = None

    # update data of cell
    def update(self, f: float, g: float, h: float, parent: CPair) -> None:
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent


class PathFinder:
    def __init__(self, board: List[List[Cell]]) -> None:
        self.board = board

    # heuristic function
    def h(self, pos: CPair, goal: CPair) -> float:
        return math.sqrt(pow(goal.row - pos.row, 2) + pow(goal.col - pos.col, 2))

    # start pathfinding
    def start(self, start: CPair, goal: CPair, initialDir: int = -1) -> List[CPair]:
        # initialise open list
        openList: List[CPair] = []

        # initialise close list
        closedList: List[List[bool]] = [[False for j in BOARD.COL] for i in BOARD.ROW]

        # initialise data list
        dataList: List[List[PFDataCell]] = [[PFDataCell() for j in BOARD.COL] for i in BOARD.ROW]

        # update lists with starting position
        openList.put(start)
        dataList[start.row][start.col].update(0, 0, 0, start)

        # maintain lowest score for out of bounds pathfinding
        nearestPos: CPair = start
        lowestScore: float = math.inf

        # start A* algorithm
        while not openList.empty():
            searchPos: CPair = openList.pop(0)

            # maintain closed list
            closedList[searchPos.row][searchPos.col] = True

            # search successors
            for dir, succ in self.board[searchPos.row][searchPos.col].adj.items():
                if succ is None:
                    continue

                # apply ghost pathfinding restrictions
                if initialDir != -1:
                    if initialDir == DIR.getOpposite(dir) and searchPos == start:
                        continue

                    if initialDir == DIR.UP and searchPos in POS.GHOST_NO_UP_CELLS:
                        continue

                # rebuild path if goal is reached
                if succ.coords == goal:
                    return self.makePath(goal, dataList)

                # update cell data
                else:
                    g: int = dataList[searchPos.row][searchPos.col].g + 1
                    h: float = self.h(succ.coords, goal)
                    f: float = g + h

                    # put successor into openlist if the f score is better
                    if dataList[succ.coords.row][succ.coords.col].f > f:
                        openList.append(succ.coords)

                        dataList[succ.coords.row][succ.coords.col].update(f, g, h, searchPos)

                    # update nearest pos:
                    if h < lowestScore:
                        lowestScore = h
                        nearestPos = succ.coords

        # return path to closest position     
        return self.makePath(nearestPos, dataList)

    # reconstruct path from weighted state
    def makePath(self, goal: CPair, dataList: List[List[PFDataCell]]) -> List[Cell]:
        path: List[CPair] = []

        parent = goal
        while parent != dataList[parent.row][parent.col].parent:
            path.insert(0, parent)
            parent = dataList[parent.row][parent.col].parent

        return path
