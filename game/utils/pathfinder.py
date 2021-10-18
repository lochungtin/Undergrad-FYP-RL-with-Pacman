from typing import List
from queue import PriorityQueue
import math

from data import BOARD, POS, REP
from game.utils.path import Path
from game.utils.pathcell import PathCell
from game.utils.pathcoordinate import PathCPair
from utils.coordinate import CPair


class PathFinder:
    # heuristic function
    def h(self, pos: CPair, goal: CPair) -> float:
        return math.sqrt(pow(goal.row - pos.row, 2) + pow(goal.col - pos.col, 2))

    # pathfind function (a* path finding with ordered direction exploration)
    def start(self, start: CPair, goal: CPair) -> Path:
        # create closed list and weighted list
        closedList: List[List[bool]] = []
        weightedList: List[List[PathCell]] = []
        for _ in range(BOARD.row):
            cRow: List[bool] = []
            wRow: List[PathCell] = []

            for _ in range(BOARD.col):
                cRow.append(False)
                wRow.append(PathCell())

            closedList.append(cRow)
            weightedList.append(wRow)

        # initialise parameters
        curPos: CPair = start
        weightedList[curPos.row][curPos.col].update(0, 0, 0, start)

        # create open list
        openList: PriorityQueue[PathCPair] = PriorityQueue()
        openList.put(PathCPair(curPos, 0))

        # start a*
        while not openList.empty():
            top: PathCPair = openList.get()

            closedList[top.cpair.row][top.cpair.col] = True

            for neighbour in top.cpair.getValidNeighbours():
                nX, nY = neighbour.row, neighbour.col

                # pass if neighbour is a wall
                if REP.isWall(REP.BOARD[nX][nY]):
                    continue

                # return path if goal is reached
                if neighbour == goal:
                    weightedList[nX][nY].parent = top.cpair

                    path: Path = self.reconstructPath(goal, weightedList)
                    path.insert(start)

                    return path

                # update cell weights
                else:
                    g: float = weightedList[top.cpair.row][top.cpair.col].g + 1
                    h: float = self.h(neighbour, goal)
                    f: float = g + h

                    if weightedList[nX][nY].f == -1 or weightedList[nX][nY].f > f:
                        # put successor into open list
                        openList.put(PathCPair(neighbour, f))

                        # update details of neighboue
                        weightedList[nX][nY].update(f, g, h, top.cpair)

    # reconstruct path from weighted state
    def reconstructPath(self, goal: CPair, weightedState: List[List[PathCell]]) -> Path:
        path = Path()

        parent = goal
        while parent != weightedState[parent.row][parent.col].parent:
            path.insert(parent)
            parent = weightedState[parent.row][parent.col].parent

        return path

p = PathFinder()
print(p.start(POS.LEFT_LOOP, POS.RIGHT_LOOP))