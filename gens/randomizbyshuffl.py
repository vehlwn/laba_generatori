from .basegenerator import BaseGenerator
from uniformdist import UniformIntDistribution


class RandomizeByShuffleM(BaseGenerator):
    """Knuth, vol 2, par 3.2.2 Other methods, Algorithm M, pp 33.
    """

    def __init__(self, gen_value: BaseGenerator, gen_index: BaseGenerator, k=100):
        self.__gen_value = gen_value
        self.__gen_index = gen_index
        self.__state = [self.__gen_value() for i in range(k)]

    def min(self):
        return self.__gen_value.min()

    def max(self):
        return self.__gen_value.max()

    def entropy(self):
        return self.__gen_value.entropy()

    def __call__(self):
        index_dist = UniformIntDistribution(0, len(self.__state) - 1)
        j = index_dist(self.__gen_index)
        ret = self.__state[j]
        self.__state[j] = self.__gen_value()
        return ret

    def __str__(self):
        return f"state = {self.__state}"


class RandomizeByShuffleB(BaseGenerator):
    """Knuth, vol 2, par 3.2.2 Other methods, Algorithm M, pp 34.
    """

    def __init__(self, gen: BaseGenerator, k=100):
        self.__gen = gen
        self.__state = [self.__gen() for i in range(k)]

    def min(self):
        return self.__gen.min()

    def max(self):
        return self.__gen.max()

    def entropy(self):
        return self.__gen.entropy()

    def __call__(self):
        index_dist = UniformIntDistribution(0, len(self.__state) - 1)
        j = index_dist(self.__gen)
        ret = self.__state[j]
        self.__state[j] = self.__gen()
        return ret

    def __str__(self):
        return f"state = {self.__state}"
