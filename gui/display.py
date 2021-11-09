from game.game import Game


class Display:
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def rerender(self) -> None:
        return