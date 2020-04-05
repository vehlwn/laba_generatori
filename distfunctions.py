import math


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
    while a < b and i < 100:
        x = a * 0.5 + b * 0.5
        # Median less than machine epsilon between a, b.
        if x == b or x == a:
            break
        v = F(x)
        # Find supremum: if v == u shift edge to the right.
        if v <= u:
            a = x
        else:
            b = x
        i += 1
    return a
