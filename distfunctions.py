import math
import pdb
import sys


def invCdf(F, u: float) -> float:
    """Returns such x ~ F that integral F(x) == u.
    """
    if u <= 0.0:
        return -math.inf
    if u >= 1.0:
        return math.inf
    a, b = 0.0, 1.0
    # Find bounds where x lies.
    i = 1
    while F(a) > u:
        a -= i
        i *= 2
    i = 1
    while F(b) < u:
        b += i
        i *= 2
    i = 0
    d = b - a
    w = int(math.ceil(sys.float_info.mant_dig * math.log2(sys.float_info.radix)))
    for i in range(w):
        d /= 2
        x = a + d
        v = F(x)
        # Find supremum: if v == u shift edge to the right.
        if v <= u:
            a = x
    return a
