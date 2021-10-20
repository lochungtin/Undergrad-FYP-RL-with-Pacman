from copy import deepcopy
from tkinter import Canvas
from typing import List, Tuple
import itertools

from data import DATA, REP
from game.components.movable.ghosts.blinky import Blinky
from game.components.movable.ghosts.clyde import Clyde
from game.components.movable.ghosts.ghost import Ghost
from game.components.movable.ghosts.inky import Inky
from game.components.movable.ghosts.pinky import Pinky
from game.components.movable.pacman import Pacman
from game.components.stationary.pellet import Pellet, PowerPellet, TypePellet
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Game:
    def __init__(self) -> None:
        # set state from template
        self.state: List[List[int]] = deepcopy(REP.BOARD)

        # initialise pathfinder
        self.pathfinder: PathFinder = PathFinder()

        # create movables
        self.pacman: Pacman = Pacman()
        self.blinky: Ghost = Blinky(self.pathfinder)
        self.inky: Ghost = Inky(self.pathfinder)
        self.clyde: Ghost = Clyde(self.pathfinder)
        self.pinky: Ghost = Pinky(self.pathfinder)

        self.ghosts: List[Ghost] = [
            self.blinky,
            self.inky,
            self.clyde,
            self.pinky,
        ]

        # update state
        for movable in itertools.chain([self.pacman], self.ghosts):
            self.state[movable.pos.row][movable.pos.col] = movable.repId

        # create pellets and update state
        self.pellets: List[List[TypePellet]] = []
        for rowIndex, gridRow in enumerate(REP.PELLET_BOARD):
            row: List[TypePellet] = []
            for colIndex, cell in enumerate(gridRow):
                if cell == REP.EMPTY:
                    row.append(None)
                elif cell == REP.PELLET:
                    row.append(Pellet(CPair(rowIndex, colIndex)))
                    self.state[rowIndex][colIndex] = REP.PELLET
                else:
                    row.append(PowerPellet(CPair(rowIndex, colIndex)))
                    self.state[rowIndex][colIndex] = REP.PWRPLT

            self.pellets.append(row)

        self.pelletCount = DATA.TOTAL_PELLET_COUNT + DATA.TOTAL_PWRPLT_COUNT

        # initialise countdown step count and set ghost schedule index
        self.stepCount: int = DATA.TOTAL_STEP_COUNT
        self.ghostSchedule: int = 0

        self.ghostFrightenedCount: int = -1

        # set canvas to None as default
        self.canvas: Canvas = None

    # set canvas object
    def setCanvas(self, canvas: Canvas) -> None:
        self.canvas = canvas

    # proceed to next time step
    def nextStep(self) -> Tuple[bool, bool]:
        # update pacman location
        pCurPos, pPrevPos = self.pacman.getNextPos(self.state)
        prevState = self.state[pCurPos.row][pCurPos.col]

        self.state[pPrevPos.row][pPrevPos.col] = REP.EMPTY
        self.state[pCurPos.row][pCurPos.col] = REP.PACMAN

        # check collision to trigger gameover return
        for ghost in self.ghosts:
            if pCurPos == ghost.pos:
                return True, False, False

        # perform actions if new position had pellets
        atePellet: bool = prevState == REP.PELLET or prevState == REP.PWRPLT
        if atePellet:
            # set ghost mode to frightened
            if prevState == REP.PWRPLT:
                for ghost in self.ghosts:
                    ghost.isFrightened = True

                self.ghostFrightenedCount = DATA.GHOST_FRIGHTENED_STEP_COUNT

            # update pellet and pellet count
            pellet: TypePellet = self.pellets[pCurPos.row][pCurPos.col]
            if pellet != None and pellet.valid:
                id = pellet.destroy()

                # update canvas if present
                if self.canvas != None:
                    self.canvas.delete(id)

                self.pelletCount -= 1

            # end game if all pellets have been eaten
            if self.pelletCount == 0:
                return True, True, False

        # update ghosts' locations
        for ghost in self.ghosts:
            gCurPos, gPrevPos = ghost.getNextPos(self.state)

            # check collision to trigger gameover return
            if gCurPos == pCurPos:
                return True, False, False

            pellet: TypePellet = self.pellets[gPrevPos.row][gPrevPos.col]
            if pellet != None and pellet.valid:
                self.state[gPrevPos.row][gPrevPos.col] = pellet.repId
            else:
                self.state[gPrevPos.row][gPrevPos.col] = REP.EMPTY

            self.state[gCurPos.row][gCurPos.col] = ghost.repId

        # update counter and ghost modes
        if self.stepCount > -1:
            self.stepCount -= 1

        if self.stepCount < DATA.GHOST_MODE_SCHEDULE[self.ghostSchedule][1]:
            self.ghostSchedule += 1

            # set all ghost to new mode
            for ghost in self.ghosts:
                ghost.mode = DATA.GHOST_MODE_SCHEDULE[self.ghostSchedule][0]

        # update frightened state
        if self.ghostFrightenedCount > -1:
            self.ghostFrightenedCount -= 1
            
            # set all ghost to not frightened after 80 time steps
            if self.ghostFrightenedCount == -1:
                for ghost in self.ghosts:
                    ghost.isFrightened = False

        return False, False, atePellet
