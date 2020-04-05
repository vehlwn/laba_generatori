import bisect
import math
import pdb
import typing


class EmpiricalCdf:
    """Returns P(data[:] <= x).
    """

    def __call__(self, x: float) -> float:
        raise NotImplementedError

    def data_size(self):
        raise NotImplementedError


class EcdfFromUnsortedData(EmpiricalCdf):

    def __init__(self, data):
        super().__init__()
        self.sorted_data = sorted(data)

    def __call__(self, x: float) -> float:
        """upper_bound - element after the last in a range of equivalents.
        """
        i = bisect.bisect_right(self.sorted_data, x)
        ret = i / len(self.sorted_data)
        return ret

    def data_size(self):
        return len(self.sorted_data)


class EcdfFromAccumulatedProbability(EmpiricalCdf):

    def __init__(self, data: typing.List[float]):
        """data - is a list of floats from 0.0 to 1.0 in nondecreasing order.
        """
        super().__init__()
        self.__accumulated = data[:]

    def __call__(self, x: float) -> float:
        if x < 0.0:
            return 0.0
        elif x >= len(self.__accumulated):
            return 1.0
        i = int(math.floor(x))
        return self.__accumulated[i]

    def __str__(self):
        return str(self.__accumulated)
