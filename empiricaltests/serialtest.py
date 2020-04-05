from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2
from uniformdist import UniformIntDistribution
import typing


class SerialTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, B. Serial test, pp 62.
    """

    class Chi2Statistic(NullHypothesisChi2):

        def __init__(self, data: typing.List[int], d: int, serie_len: int):
            super().__init__()
            super().set_v(d ** serie_len - 1)
            self.total = sum(data)
            self.p_emp = [x / self.total for x in data]
            self.expected = 1.0 / d ** serie_len

        def statistic(self):
            n = self.total
            s = 0.0
            for emp in self.p_emp:
                s += n * (emp - self.expected) ** 2 / self.expected
            return s

    class __NullHypothesisHelper:

        def test(
            self,
            data: typing.List[int],
            significance_level: float,
            d: int,
            serie_len: int,
        ):
            series_data = self.get_series_data(data, serie_len)
            g = SerialTest.Chi2Statistic(series_data, d, serie_len)
            test_result = g.test(significance_level)
            return test_result

        def get_series_data(self, data, serie_len):
            n = len(data)
            if n % serie_len != 0:
                n -= n % serie_len
            series_map = dict()
            for i in range(0, n, serie_len):
                serie = tuple(data[i: i + serie_len])
                if serie not in series_map:
                    series_map[serie] = 0
                series_map[serie] += 1
            # print(f"{series_map=}")
            return list(series_map.values())

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 0
        passed_tests = 0
        for d in range(2, 5 + 1):
            dist = UniformIntDistribution(0, d - 1)
            data = [dist(gen) for i in range(DATA_SIZE)]
            for serie_len in range(2, 5 + 1):
                print("----")
                print(f"{d=}, {serie_len=}")
                SIGNIFICANCE = 0.05
                s = SerialTest.__NullHypothesisHelper()
                test_result = s.test(data, SIGNIFICANCE, d, serie_len)
                passed_tests += test_result.value()
                print("    chi2:", test_result)
                n_tests += 1
        return passed_tests, n_tests

    def __str__(self):
        return "Serial test"

    def weight(self) -> float:
        return 0.25
