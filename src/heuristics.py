import math
from typing import Tuple

Pos = Tuple[int, int]


def manhattan(a: Pos, b: Pos) -> float:
    dl = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])               
    return dl + dc


def euclidean(a: Pos, b: Pos) -> float:
    dl = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])               
    return math.sqrt(dl ** 2 + dc ** 2) 