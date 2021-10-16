class Displayable():
    def __init__(self, pos, rep):
        self.pos = pos
        self.rep = rep
        
    # store canvas item id
    def setDiplayObj(self, obj):
        self.display = obj
