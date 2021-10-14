from tkinter import *

from constants import *
from game import Game


class App:
    def __init__(self):
        # create application object
        self.main = Tk()
        # bind key hanlders
        self.main.bind('<Up>', self.keyUp)
        self.main.bind('<Down>', self.keyDown)
        self.main.bind('<Left>', self.keyRight)
        self.main.bind('<Right>', self.keyLeft)
        self.main.bind('<space>', self.keyDown)
        # create canvas object
        self.canvas = Canvas(
            self.main,
            width=DIM.GBL_W,
            height=DIM.GBL_H,
            background='#1E1E1E',
            highlightthickness=0,
        )
        self.canvas.pack()

        # initialise game object
        self.game = Game()

    # keystroke handlers
    def keyUp(self, event):
        self.handleKey(DIR.UP)

    def keyDown(self, event):
        self.handleKey(DIR.DW)

    def keyRight(self, event):
        self.handleKey(DIR.RT)

    def keyLeft(self, event):
        self.handleKey(DIR.LF)

    def keySpace(self, event):
        print('S')

    def handleKey(self, keyID):
        print(keyID)

    # update canvas
    def updateCanvas(self):
        # clear
        self.canvas.delete('all')

        for row in range(BOARD.row):
            for col in range(BOARD.col):
                rep = self.game.getState()[row][col]

                positioner = DIM.CELL + DIM.GAP
                x0 = col * positioner
                y0 = row * positioner
                x1 = x0 + DIM.CELL
                y1 = y0 + DIM.CELL

                if rep == REP.ORB:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[REP.EMPTY], outline=''
                    )
                    self.canvas.create_rectangle(
                        x0 + DIM.PAD_ORB,
                        y0 + DIM.PAD_ORB,
                        x1 - DIM.PAD_ORB,
                        y1 - DIM.PAD_ORB,
                        fill=REP.COLOR_MAP[rep],
                        outline='',
                    )
                elif rep == REP.PWRPLT:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[REP.EMPTY], outline=''
                    )
                    self.canvas.create_rectangle(
                        x0 + DIM.PAD_PWRPLT,
                        y0 + DIM.PAD_PWRPLT,
                        x1 - DIM.PAD_PWRPLT,
                        y1 - DIM.PAD_PWRPLT,
                        fill=REP.COLOR_MAP[rep],
                        outline='',
                    )
                elif rep == REP.DOOR:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[REP.EMPTY], outline=''
                    )
                    self.canvas.create_rectangle(
                        x0,
                        y0 + DIM.PAD_DOOR,
                        x1,
                        y1 - DIM.PAD_DOOR,
                        fill=REP.COLOR_MAP[rep],
                        outline='',
                    )
                else:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=REP.COLOR_MAP[rep], outline=''
                    )

    # start app
    def run(self):
        # run main loop of application
        self.updateCanvas()
        self.main.mainloop()
