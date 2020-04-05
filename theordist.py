import random


def cdf_theor_uniform(x: float, a: float, b: float):
    return (x - a) / (b - a)


def pdf_theor_uniform(x: float, a: float, b: float):
    if x < a or x > b:
        return 0.0
    return 1.0 / (b - a)
