import math
import pdb
import sys
import typing


def invCdf(F: typing.Callable[[float], float], u: float) -> float:
    """Returns such x ~ F that integral F(x) == u.
    """
    if u <= 0.0:
        return -math.inf
    if u >= 1.0:
        return math.inf
    a, b = 0.0, 1.0
    # Find bounds where x lies.
    i = 1.0
    while F(a) > u:
        a -= i
        i *= 2.0
    i = 1.0
    while F(b) < u:
        b += i
        i *= 2.0
    d = b - a
    w = 0
    while a + d != a:
        d /= 2.0
        x = a + d
        v = F(x)
        # Find supremum: if v == u shift edge to the right.
        if v <= u:
            a = x
        w += 1
    return a


def main():
    def cdf(x: float) -> float:
        x0 = 0
        mu = 1
        return 1.0 / math.pi * math.atan((x - x0) / mu) + 1.0 / 2

    u = 0.9999
    x = invCdf(cdf, u)
    v = cdf(x)
    print(f"{x=}")
    print(f"{v=}")
    assert math.isclose(u, v)


if __name__ == "__main__":
    main()
