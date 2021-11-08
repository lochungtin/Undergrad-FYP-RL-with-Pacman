class Gene:
    def __init__(
        self, inNode: int, outNode: int, weight: float, enabled: bool, innov: int
    ) -> None:
        self.inNode: int = inNode
        self.outNode: int = outNode
        self.weight: float = weight
        self.enabled: bool = enabled
        self.innov: int = innov

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "[i:{}, o:{}, w:{}{}, e:{}, v:{}]".format(
            self.inNode,
            self.outNode,
            (self.weight > 0) * "+",
            round(self.weight, 3),
            self.enabled * 1,
            self.innov,
        )
