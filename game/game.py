from tkinter import Canvas
from typing import List, Tuple
import itertools

from data import DATA, GHOST_MODE, POS, REP
from game.components.movable.ghosts.blinky import Blinky
from game.components.movable.ghosts.clyde import Clyde
from game.components.movable.ghosts.ghost import Ghost
from game.components.movable.ghosts.inky import Inky
from game.components.movable.ghosts.pinky import Pinky
from game.components.movable.pacman import Pacman
from game.components.stationary.pellet import Pellet, PowerPellet, TypePellet
from utils.coordinate import CPair


class Game:
    def __init__(self) -> None:
        # set state from template
        self.state: List[List[int]] = REP.BOARD

        # create movables
        self.pacman: Pacman = Pacman(POS.PACMAN)
        self.blinky: Ghost = Blinky(POS.BLINKY)
        self.inky: Ghost = Inky(POS.INKY)
        self.clyde: Ghost = Clyde(POS.CLYDE)
        self.pinky: Ghost = Pinky(POS.PINKY)

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

        # set canvas to None as default
        self.canvas: Canvas = None

    # set canvas object
    def setCanvas(self, canvas: Canvas) -> None:
        self.canvas = canvas

    # proceed to next time step
    def nextStep(self) -> Tuple[bool, bool]:
        # update pacman location
        pPrevPos, pCurPos = self.pacman.getNextPos(self.state)
        prevState = self.state[pCurPos.row][pCurPos.col]

        self.state[pPrevPos.row][pPrevPos.col] = REP.EMPTY
        self.state[pCurPos.row][pCurPos.col] = REP.PACMAN

        # perform actions if new position had pellets
        if prevState == REP.PELLET or prevState == REP.PWRPLT:
            # set ghost mode to frightened
            if prevState == REP.PWRPLT:
                for ghost in self.ghosts:
                    ghost.setMode(
                        GHOST_MODE.FRIGHTENED, DATA.GHOST_FRIGHTENED_STEP_COUNT
                    )

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
                return True, False

        # check gameover
        pNeighbours: List[CPair] = pCurPos.getValidNeighbours()
        for neighbour in pNeighbours:
            if REP.isGhost(self.state[neighbour.row][neighbour.col]):
                return True, True

        # update ghosts' locations
        for ghost in self.ghosts:
            gPrevPos, gCurPos = ghost.getNextPos(self.state)

            pellet: TypePellet = self.pellets[gPrevPos.row][gPrevPos.col]
            if pellet != None and pellet.valid:
                self.state[gPrevPos.row][gPrevPos.col] = pellet.repId
            else:
                self.state[gPrevPos.row][gPrevPos.col] = REP.EMPTY

            self.state[gCurPos.row][gCurPos.col] = ghost.repId

        # check gameover
        for neighbour in pNeighbours:
            if REP.isGhost(self.state[neighbour.row][neighbour.col]):
                return True, True

        return False, False
