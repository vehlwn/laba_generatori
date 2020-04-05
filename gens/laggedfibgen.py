from .basegenerator import BaseGenerator
from gens.linearcongruentialgen import Lcg


class LaggedFibGen(BaseGenerator):
    """X_n = (X_{n-L} + X_{n-K}) % m, L < K.
    If m = 2**e period is 2**(e - 1) * (2**K - 1).
    L     K
    24    55
    30    127
    37    100
    38    89
    83    258
    107   378
    273   607
    576   3217
    1029  2281
    4187  9689
    7083  19937
    9739  23209
    """

    def __init__(self, seed=0, L=37, K=100, m=2 ** 32):
        super().__init__()
        self.__L = L
        self.__K = K
        self.__m = m
        lcg_gen = Lcg(seed)
        self.__state = [lcg_gen() for i in range(self.__K)]
        self.__j = self.__L - 1
        self.__n = self.__K - 1

    def min(self):
        return 0

    def max(self):
        return self.__m - 1

    def __call__(self):
        # Knuth, vol 2, par 3.2.2 Other methods, Algorithm A Additive number
        # generator, pp 28.
        self.__state[self.__n] = (
            self.__state[self.__n] + self.__state[self.__j]
        ) % self.__m
        ret = self.__state[self.__n]
        if self.__j == 0:
            self.__j = self.__K
        if self.__n == 0:
            self.__n = self.__K
        self.__j -= 1
        self.__n -= 1
        return ret

    def entropy(self):
        ret = self.max().bit_length()
        if (1 << ret) - 1 > self.max():
            ret -= 1
        return ret

    def __str__(self):
        return (
            f"L = {self.__L}"
            f"; K = {self.__K}"
            f"; m = {self.__m}"
            f"; j = {self.__j}"
            f"; n = {self.__n}"
            f"; state = {self.__state}"
        )
