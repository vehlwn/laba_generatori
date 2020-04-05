from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2
from uniformdist import UniformIntDistribution
import pdb
import scipy.stats
import typing


class BirthdaySpacingTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, J. Birthday spacing test, pp 71.
    """

    class StatisticHelper(NullHypothesisChi2):

        def __init__(self, collisions: typing.List[int], m_urns: int, n_balls: int):
            super().__init__()
            if m_urns < n_balls:
                raise ValueError(
                    f"m_urns must be greater or equal n_balls ({m_urns} < {n_balls})"
                )
            self.m_urns = m_urns
            self.n_balls = n_balls
            self.total = sum(collisions)
            self.collisions = [x / self.total for x in collisions]
            self.mu = self.n_balls ** 3 / 4 / self.m_urns
            print(f"mu={self.mu}")
            super().set_v(len(self.collisions) - 1)

        def statistic(self):
            # Poisson approximation.
            # pdb.set_trace()
            max_collisions = len(self.collisions) - 1
            expected = [
                scipy.stats.poisson.pmf(r, self.mu) for r in range(0, max_collisions)
            ] + [1.0 - scipy.stats.poisson.cdf(max_collisions - 1, self.mu)]
            expected_num = [self.total * x for x in expected]
            print(f"{expected_num=}")

            s = 0
            for i, x in enumerate(self.collisions):
                s += self.total * (x - expected[i]) ** 2 / expected[i]
            return s

    class __NullHypothesisHelper:

        def __init__(
            self, m_urns: int, n_balls: int, max_collisions: int, n_times: int
        ):
            self.m_urns = m_urns
            self.n_balls = n_balls
            self.max_collisions = max_collisions
            self.n_times = n_times

        def test(self, gen: BaseGenerator, significance_level: float):
            collisions = self.__get_collision_data(gen)
            print(f"{collisions=}")
            # pdb.set_trace()
            g = BirthdaySpacingTest.StatisticHelper(
                collisions, self.m_urns, self.n_balls
            )
            test_result = g.test(significance_level)
            return test_result

        def __count_collisions(self, data: typing.List[int]) -> int:
            # pdb.set_trace()
            sorted_data = sorted(data)
            spacings = []
            for i in range(1, len(sorted_data)):
                spacings.append(sorted_data[i] - sorted_data[i - 1])
            spacings.append(sorted_data[0] + self.m_urns - sorted_data[-1])
            spacings.sort()

            prev_spacing = spacings[0]
            ret = 0
            for a in spacings[1:]:
                if a == prev_spacing:
                    ret += 1
                else:
                    prev_spacing = a
            return ret

        def __get_collision_data(self, gen: BaseGenerator):
            count = [0] * (self.max_collisions + 1)

            def update_count(c: int):
                if c >= self.max_collisions:
                    count[self.max_collisions] += 1
                else:
                    count[c] += 1

            # pdb.set_trace()
            dist = UniformIntDistribution(0, self.m_urns - 1)
            for i in range(self.n_times):
                data = [dist(gen) for j in range(self.n_balls)]
                c = self.__count_collisions(data)
                update_count(c)

            return count

    def perform(self, gen: BaseGenerator, DATA_SIZE: int = None):
        n_tests = 0
        passed_tests = 0
        for m_urns, n_balls, max_collisions in [
            (2 ** 22, 2 ** 8, 4),
            (2 ** 25, 2 ** 9, 4),
            (2 ** 28, 2 ** 10, 4),
            (2 ** 31, 2 ** 11, 4),
        ]:
            print("----")
            print(f"{m_urns=}, {n_balls=}")
            SIGNIFICANCE = 0.05
            s = BirthdaySpacingTest.__NullHypothesisHelper(
                m_urns, n_balls, max_collisions, 1000
            )
            test_result = s.test(gen, SIGNIFICANCE)
            passed_tests += test_result.value()
            print("    chi2:", test_result)
            n_tests += 1
        return passed_tests, n_tests

    def __str__(self):
        return "Birthday spacing test"

    def weight(self) -> float:
        return 20
