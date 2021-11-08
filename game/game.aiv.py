from game.game import Game


class AIV(Game):
    def __init__(self, enableGhost: bool = True, enablePwrPlt: bool = True) -> None:
        super().__init__(enableGhost=enableGhost, enablePwrPlt=enablePwrPlt)