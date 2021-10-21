from typing import List
from queue import PriorityQueue
import math

from data import BOARD, DIR, POS, REP
from game.utils.path import Path
from game.utils.pathcell import PathCell
from game.utils.pathcoordinate import PathCPair
from utils.coordinate import CPair


class PathFinder:
    # heuristic function
    def h(self, pos: CPair, goal: CPair) -> float:
        return math.sqrt(pow(goal.row - pos.row, 2) + pow(goal.col - pos.col, 2))

    # pathfind function (a* path finding with ordered direction exploration)
    def start(self, start: CPair, goal: CPair, direction: int) -> Path:
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

        # maintain lowest score for out of bounds pathfinding
        nearestPos: CPair = start
        lowestScore: float = math.inf

        # start a*
        while not openList.empty():
            top: PathCPair = openList.get()
            searchPos: CPair = top.cpair

            closedList[searchPos.row][searchPos.col] = True

            for index, neighbour in enumerate(searchPos.getNeighbours()):
                # disallow expansion to opposite direction or current motion
                if searchPos == start and DIR.getOpposite(direction) == index:
                    continue

                # ignore areas that ghosts cant go up
                if (
                    searchPos == POS.GHOST_NO_UP_1
                    or searchPos == POS.GHOST_NO_UP_2
                    or searchPos == POS.GHOST_NO_UP_3
                    or searchPos == POS.GHOST_NO_UP_4
                ) and index == 0:
                    continue

                nX, nY = neighbour.row, neighbour.col

                # pass if neighbour is a wall
                if REP.BOARD[nX][nY] == REP.WALL:
                    continue

                # return path if goal is reached
                if neighbour == goal:
                    weightedList[nX][nY].parent = searchPos

                    return self.reconstructPath(goal, weightedList)

                # update cell weights
                else:
                    g: float = weightedList[searchPos.row][searchPos.col].g + 1
                    h: float = self.h(neighbour, goal)
                    f: float = g + h

                    # if neighbour is closer to finish
                    if weightedList[nX][nY].f == -1 or weightedList[nX][nY].f > f:
                        # put successor into open list
                        openList.put(PathCPair(neighbour, f))

                        # update details of neighbour
                        weightedList[nX][nY].update(f, g, h, searchPos)

                    # update nearest pos
                    if h < lowestScore:
                        lowestScore = h
                        nearestPos = neighbour

        return self.reconstructPath(nearestPos, weightedList)  

    # reconstruct path from weighted state
    def reconstructPath(self, goal: CPair, weightedList: List[List[PathCell]]) -> Path:
        path = Path()

        parent = goal
        while parent != weightedList[parent.row][parent.col].parent:
            path.insert(parent)
            parent = weightedList[parent.row][parent.col].parent

        return path
