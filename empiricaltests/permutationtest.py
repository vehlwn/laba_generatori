from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2
from uniformdist import UniformRealDistribution
import math
import numpy
import pdb
import typing


def _analyze_permutation(data) -> int:
    """Algorithm P (Analyze a permutation), pp 65.
    """
    data = list(data[:])
    t = len(data)
    f = 0
    for r in range(t - 1, 0, -1):
        s = numpy.argmax(data[0: r + 1])
        f = (r + 1) * f + s
        data[r], data[s] = data[s], data[r]
    return f


class PermutationTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, F. Permutation test, pp 65.
    """

    class Chi2Statistic(NullHypothesisChi2):

        def __init__(self, data: typing.List[int], serie_len: int):
            super().__init__()
            k_categories = math.factorial(serie_len)
            super().set_v(k_categories - 1)
            self.total = sum(data)
            self.p_emp = [x / self.total for x in data]
            self.expected = 1.0 / k_categories

        def statistic(self):
            # print(f"expected={self.expected * self.total}")
            # print(f"p_emp={self.p_emp}")
            n = self.total
            s = 0.0
            for i in range(len(self.p_emp)):
                s += n * (self.p_emp[i] - self.expected) ** 2 / self.expected
            return s

    class __NullHypothesisHelper:

        def test(self, data, significance_level: float, serie_len: int):
            # pdb.set_trace()
            series_data = self.get_series_data(data, serie_len)
            g = PermutationTest.Chi2Statistic(series_data, serie_len)
            test_result = g.test(significance_level)
            return test_result

        def get_series_data(self, data, serie_len: int):
            n = len(data)
            if n % serie_len != 0:
                n -= n % serie_len
            series_map = dict()
            for i in range(0, n, serie_len):
                serie = tuple(data[i: i + serie_len])
                serie_index = _analyze_permutation(serie)
                if serie_index not in series_map:
                    series_map[serie_index] = 0
                series_map[serie_index] += 1
            # print(f"{series_map=}")
            return list(series_map.values())

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 0
        passed_tests = 0
        dist = UniformRealDistribution(0.0, 1.0)
        data = [dist(gen) for i in range(DATA_SIZE)]
        for serie_len in range(2, 6 + 1):
            print("----")
            print(f"{serie_len=}")
            SIGNIFICANCE = 0.05
            s = PermutationTest.__NullHypothesisHelper()
            test_result = s.test(data, SIGNIFICANCE, serie_len)
            passed_tests += test_result.value()
            print("    chi2:", test_result)
            n_tests += 1

        return passed_tests, n_tests

    def __str__(self):
        return "Permutation test"

    def weight(self) -> float:
        return 1
