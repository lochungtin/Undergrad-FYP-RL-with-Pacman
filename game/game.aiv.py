from game.game import Game


class AIV(Game):
    def __init__(self,  enableGhost: bool = True, enablePwrPlt: bool = True) -> None:
        super().__init__(enablePacman=True, enableGhost=enableGhost, enablePwrPlt=enablePwrPlt)