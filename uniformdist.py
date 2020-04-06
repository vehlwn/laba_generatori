from gens.basegenerator import BaseGenerator
from gens.bitsengine import BitsEngine
import math
import pdb
import sys


class BaseUniformDistribution:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, gen: BaseGenerator):
        raise NotImplementedError

    def params(self):
        return (self.a, self.b)


class UniformIntDistribution(BaseUniformDistribution):
    """Integer distribution between [a, b].
    """

    def __init__(self, a, b):
        super().__init__(a, b)
        self.__e = BitsEngine()

    def __call__(self, gen):
        if self.b <= self.a:
            return self.a
        params_range = self.b - self.a
        w = params_range.bit_length()
        while True:
            u = self.__e(gen, w)
            if u > params_range:
                continue
            break
        return u + self.a


class UniformRealDistribution(BaseUniformDistribution):
    """Floating distribution between [a, b).
    """

    def __init__(self, a, b):
        super().__init__(a, b)
        self.__w = int(
            math.ceil(sys.float_info.mant_dig *
                      math.log2(sys.float_info.radix))
        )
        self.__e = BitsEngine()

    def __call__(self, gen):
        if self.b <= self.a:
            return self.a
        params_range = self.b - self.a
        u = self.__e(gen, self.__w) * math.pow(2.0, -self.__w)
        return u * params_range + self.a
