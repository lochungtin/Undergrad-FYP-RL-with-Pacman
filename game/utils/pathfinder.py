from copy import deepcopy
from queue import PriorityQueue
from typing import List, Tuple
import math

from data.config import BOARD, POS
from data.data import BOARD
from game.utils.cell import Cell
from utils.coordinate import CPair
from utils.direction import DIR


class PFDataCell:
    def __init__(self) -> None:
        self.f: float = float("inf")
        self.g: float = -1
        self.h: float = -1
        self.parent: CPair = CPair(-1, -1)

    # update data of cell
    def update(self, f: float, g: float, h: float, parent: CPair) -> None:
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent

    def __repr__(self) -> str:
        return "f: {} g: {} h: {} | p: {}".format(self.f, self.g, self.h, self.parent)


class PathFinder:
    def __init__(self, board: List[List[Cell]]) -> None:
        self.board = board

    # heuristic function
    def h(self, pos: CPair, goal: CPair) -> float:
        return math.sqrt(pow(goal.row - pos.row, 2) + pow(goal.col - pos.col, 2))

    # start pathfinding
    def start(self, start: CPair, goal: CPair, initialDir: int = -1) -> List[CPair]:
        # fix goal location until valid
        if not BOARD.isValidPos(goal) or self.board[goal.row][goal.col].isWall:
            adjGoal: CPair = deepcopy(goal)

            adjGoal.row = max(adjGoal.row, 1)
            adjGoal.row = min(adjGoal.row, BOARD.ROW - 2)

            adjGoal.col = max(adjGoal.col, 1)
            adjGoal.col = min(adjGoal.col, BOARD.COL - 2)

            goal = adjGoal

            if self.board[adjGoal.row][adjGoal.col].isWall:
                for dir in DIR.getList():
                    newGoal: CPair = adjGoal.move(dir)
                    if self.board[newGoal.row][newGoal.col].isWall:
                        goal = newGoal
                        break

        # return minimal path if adjusted goal is the starting position
        if start == goal:
            return [goal]            

        # initialise open list
        openList: PriorityQueue(Tuple[float, CPair]) = PriorityQueue()

        # initialise close list
        closedList: List[List[bool]] = [[False for j in range(BOARD.COL)] for i in range(BOARD.ROW)]

        # initialise data list
        dataList: List[List[PFDataCell]] = [[PFDataCell() for j in range(BOARD.COL)] for i in range(BOARD.ROW)]

        # update lists with starting position
        openList.put((0, start))
        dataList[start.row][start.col].update(0, 0, 0, start)

        # maintain lowest score for out of bounds pathfinding
        nearestPos: CPair = start
        lowestScore: float = float("inf")

        # start A* algorithm
        while not openList.empty():
            searchPos: CPair = openList.get(0)[1]

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

                    if dir == DIR.UP and succ.coords in POS.GHOST_NO_UP_CELLS:
                        continue

                sCPair: CPair = succ.coords
                sR: int = sCPair.row
                sC: int = sCPair.col

                # rebuild path if goal is reached
                if succ.coords == goal:
                    dataList[sR][sC].parent = searchPos
                    return self.makePath(goal, dataList)

                # update cell data
                else:
                    g: int = dataList[searchPos.row][searchPos.col].g + 1
                    h: float = self.h(sCPair, goal)
                    f: float = g + h

                    # put successor into openlist if the f score is better
                    if dataList[sR][sC].f > f:
                        openList.put((f, sCPair))
                        dataList[sR][sC].update(f, g, h, searchPos)

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
