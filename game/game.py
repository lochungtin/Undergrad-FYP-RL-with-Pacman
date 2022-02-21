from copy import deepcopy
from tkinter import Canvas
from typing import List, Tuple

from agents.base import DirectionAgent, GhostAgent
from data.config import CONFIG
from data.data import DATA, POS, REP
from game.components.pellet import Pellet, PowerPellet, PelletType
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair


class Game:
    def __init__(
        self,
        pacman: DirectionAgent,
        blinky: GhostAgent = None,
        inky: GhostAgent = None,
        clyde: GhostAgent = None,
        pinky: GhostAgent = None,
        enablePwrPlt: bool = True,
    ) -> None:
        # save game config
        self.enablePwrPlt: bool = enablePwrPlt

        # set state from template
        self.state: List[List[int]] = deepcopy(CONFIG.BOARD)

        # initialise pathfinder
        self.pathfinder: PathFinder = PathFinder()

        # create agents
        self.pacman: DirectionAgent = pacman
        self.state[POS.PACMAN.row][POS.PACMAN.col] = REP.PACMAN

        self.ghosts: List[GhostAgent] = []

        self.blinky: GhostAgent = blinky
        if hasattr(blinky, "pos"):
            self.ghosts.append(blinky)

        self.inky: GhostAgent = inky
        if hasattr(inky, "pos"):
            self.ghosts.append(inky)

        self.clyde: GhostAgent = clyde
        if hasattr(clyde, "pos"):
            self.ghosts.append(clyde)

        self.pinky: GhostAgent = pinky
        if hasattr(pinky, "pos"):
            self.ghosts.append(pinky)

        for ghost in self.ghosts:
            self.state[ghost.pos.row][ghost.pos.col] = ghost.repId
            if ghost.isClassic:
                ghost.bindPathFinder(self.pathfinder)

        # create pellets and update state
        self.pellets: List[List[PelletType]] = []
        for rowIndex, gridRow in enumerate(CONFIG.PELLET_BOARD):
            row: List[PelletType] = []
            for colIndex, cell in enumerate(gridRow):
                if cell == REP.EMPTY:
                    row.append(None)
                elif cell == REP.PELLET:
                    row.append(Pellet(CPair(rowIndex, colIndex)))
                    self.state[rowIndex][colIndex] = REP.PELLET
                elif enablePwrPlt:
                    row.append(PowerPellet(CPair(rowIndex, colIndex)))
                    self.state[rowIndex][colIndex] = REP.PWRPLT
                else:
                    row.append(None)

            self.pellets.append(row)

        self.pelletCount: int = DATA.TOTAL_PELLET_COUNT + DATA.TOTAL_PWRPLT_COUNT * enablePwrPlt

        # initialise countdown step count and set ghost schedule index
        self.stepCount: int = DATA.TOTAL_STEP_COUNT
        self.ghostSchedule: int = 0

        self.ghostFrightenedCount: int = -1

        # game status
        self.timesteps: int = 0

        # set canvas to None as default
        self.canvas: Canvas = None

    # set canvas object
    def setCanvas(self, canvas: Canvas) -> None:
        self.canvas = canvas

    # proceed to next time step
    def nextStep(self) -> Tuple[bool, bool, bool, bool]:
        self.timesteps += 1

        # update pacman location
        pCurPos, pPrevPos, pacmanMoved = self.pacman.getNextPos(self)
        prevState = self.state[pCurPos.row][pCurPos.col]

        self.state[pPrevPos.row][pPrevPos.col] = REP.EMPTY
        self.state[pCurPos.row][pCurPos.col] = REP.PACMAN

        ateGhost: bool = False
        # handle ghost collision
        for ghost in self.ghosts:
            if pCurPos == ghost.pos:
                if not ghost.isDead:
                    if ghost.isFrightened:
                        ghost.isFrightened = False
                        ghost.isDead = True
                        ateGhost = True
                    else:
                        return True, False, False, ateGhost, pacmanMoved

        # perform actions if new position had pellets
        atePellet: bool = prevState == REP.PELLET or prevState == REP.PWRPLT
        if atePellet:
            # set ghost mode to frightened
            if prevState == REP.PWRPLT:
                for ghost in self.ghosts:
                    ghost.isFrightened = True

                self.ghostFrightenedCount = DATA.GHOST_FRIGHTENED_STEP_COUNT

            # update pellet and pellet count
            pellet: PelletType = self.pellets[pCurPos.row][pCurPos.col]
            if pellet != None and pellet.valid:
                id = pellet.destroy()

                # update canvas if present
                if self.canvas != None:
                    self.canvas.delete(id)

                self.pelletCount -= 1

            # end game if all pellets have been eaten
            if self.pelletCount == 0:
                return False, True, False, ateGhost, pacmanMoved

        # update ghosts' locations
        for ghost in self.ghosts:
            gCurPos, gPrevPos, ghostMoved = ghost.getNextPos(self)

            # handle ghost collision
            if gCurPos == pCurPos:
                if not ghost.isDead:
                    if ghost.isFrightened:
                        ghost.isFrightened = False
                        ghost.isDead = True
                        ateGhost = True
                    else:
                        return True, False, False, ateGhost, pacmanMoved

            pellet: PelletType = self.pellets[gPrevPos.row][gPrevPos.col]
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
                if ghost.isClassic:
                    ghost.mode = DATA.GHOST_MODE_SCHEDULE[self.ghostSchedule][0]

        # update frightened state
        if self.ghostFrightenedCount > -1:
            self.ghostFrightenedCount -= 1

            # set all ghost to not frightened after some time steps
            if self.ghostFrightenedCount == -1:
                for ghost in self.ghosts:
                    ghost.isFrightened = False

        return False, False, atePellet, ateGhost, pacmanMoved
