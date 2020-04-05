from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.combinatorial.numbers import stirling
from uniformdist import UniformIntDistribution
import math
import numpy
import pdb
import typing


class PockerTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, D. Poker test, pp 63.
    """

    class Chi2Statistic(NullHypothesisChi2):

        def __init__(self, data: typing.List[int], d: int):
            super().__init__()
            self.serie_len = len(data)
            super().set_v(self.serie_len - 1)
            self.total = sum(data)
            self.p_emp = [x / self.total for x in data]
            self.d = d

        def statistic(self):
            expected = [
                float(
                    factorial(self.d)
                    / factorial(self.d - r)
                    / self.d ** self.serie_len
                    * stirling(self.serie_len, r)
                )
                for r in range(1, self.serie_len + 1)
            ]
            if self.serie_len > 2:
                # Join the first two categories since the p_r for r = 1..2 is
                # very small.
                expected[1] += expected[0]
                self.p_emp[1] += self.p_emp[0]
                expected = expected[1:]
                self.p_emp = self.p_emp[1:]
            print(f"expected={list(x * self.total for x in expected)}")
            print(f"p_emp={list(x * self.total for x in self.p_emp)}")
            n = self.total
            s = 0.0
            for i in range(len(self.p_emp)):
                s += n * (self.p_emp[i] - expected[i]) ** 2 / expected[i]
            return s

    class __NullHypothesisHelper:

        def __init__(self, d: int, serie_len: int):
            self.d = d
            self.serie_len = serie_len

        def test(self, data: typing.List[int], significance_level: float):
            poker_data = self.get_poker_data(data)
            g = PockerTest.Chi2Statistic(poker_data, self.d)
            test_result = g.test(significance_level)
            return test_result

        def get_poker_data(self, data: typing.List[int]):
            count = [0] * self.serie_len

            def update_count(n_distinct):
                count[n_distinct - 1] += 1

            n = len(data)
            if n % self.serie_len != 0:
                n -= n % self.serie_len

            for i in range(0, n, self.serie_len):
                serie = tuple(data[i: i + self.serie_len])
                update_count(len(numpy.unique(serie)))

            return count

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 0
        passed_tests = 0
        for d in range(5, 10 + 1, 1):
            dist = UniformIntDistribution(0, d - 1)
            data = [dist(gen) for i in range(DATA_SIZE)]
            # serie_len must be <= d.
            for serie_len in range(5, d + 1, 1):
                print("----")
                print(f"{d=}, {serie_len=}")
                SIGNIFICANCE = 0.05
                s = PockerTest.__NullHypothesisHelper(d, serie_len)
                test_result = s.test(data, SIGNIFICANCE)
                passed_tests += test_result.value()
                print("    chi2:", test_result)
                n_tests += 1
        return passed_tests, n_tests

    def __str__(self):
        return "Poker test"

    def weight(self) -> float:
        return 1
