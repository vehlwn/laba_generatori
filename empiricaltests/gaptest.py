from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2
from uniformdist import UniformRealDistribution
import pdb
import typing


class GapTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, C. Gap test, pp 62.
    """

    class Chi2Statistic(NullHypothesisChi2):

        def __init__(self, data: typing.List[int], alph: float, beta: float):
            super().__init__()
            super().set_v(len(data) - 1)
            self.total = sum(data)
            self.p_emp = [x / self.total for x in data]
            self.p = beta - alph

        def statistic(self):
            expected = [
                self.p * (1.0 - self.p) ** x for x in range(len(self.p_emp) - 1)
            ]
            expected.append((1.0 - self.p) ** len(self.p_emp))
            # print(f"{expected=}")
            # print(f"p_emp={self.p_emp}")
            n = self.total
            s = 0.0
            for i in range(len(self.p_emp)):
                s += n * (self.p_emp[i] - expected[i]) ** 2 / expected[i]
            return s

    class __NullHypothesisHelper:

        def __init__(self, n_gaps: int, max_gap_length: int, alph: float, beta: float):
            self.n_gaps = n_gaps
            self.max_gap_length = max_gap_length
            self.alph = alph
            self.beta = beta

        def test(self, gen: BaseGenerator, significance_level: float):
            gap_data = self.get_gap_data(gen)
            g = GapTest.Chi2Statistic(gap_data, self.alph, self.beta)
            test_result = g.test(significance_level)
            return test_result

        def get_gap_data(self, gen: BaseGenerator):
            count = [0] * (self.max_gap_length + 1)

            def update_count(gap_len):
                if gap_len >= self.max_gap_length:
                    count[self.max_gap_length] += 1
                else:
                    count[gap_len] += 1

            dist = UniformRealDistribution(0.0, 1.0)
            for i in range(self.n_gaps):
                current_gap_len = 0
                while True:
                    u = dist(gen)
                    if self.alph <= u < self.beta:
                        update_count(current_gap_len)
                        break
                    else:
                        current_gap_len += 1
            return count

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 0
        passed_tests = 0
        for max_gap_length in [10, 15, 20]:
            for alph, beta in [
                (0.0, 0.5),
                (0.5, 1.0),
                (0.0, 0.25),
                (0.25, 0.5),
                (0.5, 0.75),
                (0.75, 1.0),
            ]:
                print("----")
                print(f"{max_gap_length=}, {alph=}, {beta=}")
                SIGNIFICANCE = 0.05
                s = GapTest.__NullHypothesisHelper(
                    DATA_SIZE, max_gap_length, alph, beta
                )
                test_result = s.test(gen, SIGNIFICANCE)
                passed_tests += test_result.value()
                print("    chi2:", test_result)
                n_tests += 1
        return passed_tests, n_tests

    def __str__(self):
        return "Gap test"

    def weight(self) -> float:
        return 2
