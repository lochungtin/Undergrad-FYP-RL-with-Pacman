from typing import Literal, Tuple

# node type literals
class NodeType:
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    HIDDEN = "HIDDEN"


class NodeGene:
    def __init__(self, config: dict[str, object]) -> None:
        self.id: int = config["id"]
        self.type: Literal["INPUT", "OUTPUT", "HIDDEN"] = config["type"]
        self.bias: float = config["bias"]

    # mutation functions
    def setBias(self, bias: float) -> None:
        self.bias = bias

    # custom string representation
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "{}: ({} | {})".format(self.id, self.bias, self.type)


class ConnGene:
    def __init__(self, config: dict[str, object]) -> None:
        if "key" in config:
            self.key: str = config["key"]
        else:
            self.key: str = ConnGene.genKey(config["inId"], config["outId"])

        if "enabled" in config:
            self.enabled: bool = config["enabled"]
        else:
            self.enabled: bool = True

        self.weight: float = config["weight"]

        if "innov" in config:
            self.innov: int = config["innov"]

    # mutation functions
    def setEnabled(self, enabled: bool) -> None:
        self.enabled = enabled

    def setWeight(self, weight: float) -> None:
        self.weight = weight

    # custom string representation
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        e = "░"
        if self.enabled:
            e = "▓"

        return "{}: ({} | {})".format(self.key, self.weight, e)

    # static methods
    # generate key string
    def genKey(inId: int, outId: int) -> str:
        return "{}-{}".format(inId, outId)

    def parseKey(key: str) -> Tuple[int, int]:
        return map(lambda n: int(n) ,key.split("-"))
