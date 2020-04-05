from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisBase
from numericaldist import EcdfFromAccumulatedProbability
from uniformdist import UniformIntDistribution
import functools
import pdb
import typing


@functools.lru_cache
def _get_A(m: int, n: int):
    """Requires a lot of time and memory.
    Tuning the Collision Test for Stringency. W.W. Tsang, L.C.K. Hui, K.P. Chow
    and C.F. Chong. The University of Hong Kong.
    """
    A = [0.0] * (n + 1)
    A[1] = 1.0
    j0 = 1
    j1 = 1
    for i in range(n - 1):
        j1 += 1
        for j in range(j1, j0 - 1, -1):
            A[j] = j / m * A[j] + (1.0 + 1.0 / m - j / m) * A[j - 1]
        if A[j0] < 1.0e-20:
            A[j0] = 0.0
            j0 += 1
        if A[j1] < 1.0e-20:
            A[j1] = 0.0
            j1 -= 1
    return (A, j0, j1)


@functools.lru_cache
def _pcoll1(m: int, n: int, c: int) -> float:
    (A, j0, j1) = _get_A(m, n)
    if n - c > j1:
        return 0.0
    if n - c < j0:
        return 1.0
    # pdb.set_trace()
    ret = A[j1]
    while n - c < j1:
        j1 -= 1
        ret += A[j1]
    return ret


class CollisionTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, I. Collision test, pp 70.
    """

    class StatisticHelper(NullHypothesisBase):

        def __init__(
            self, c_collisions: int, m_urns: int, n_balls: int, dimensions: int
        ):
            super().__init__()
            if m_urns < n_balls:
                raise ValueError(
                    f"m_urns must be greater or equal n_balls ({m_urns} < {n_balls})"
                )
            self.m_urns = m_urns
            self.n_balls = n_balls
            self.c_collisions = c_collisions
            self.dimensions = dimensions
            self.stat_ecdf = self.__gen_stat_ecdf()

        def statistic(self):
            return self.c_collisions

        def cdfStatistic(self, x):
            # Poisson approximation.
            # mu = (self.n_balls / self.dimensions) ** 2 / 2 / self.m_urns
            # return scipy.stats.poisson.cdf(x, mu)
            return self.stat_ecdf(x)

        def __gen_stat_ecdf(self):
            # pdb.set_trace()
            ar = [
                _pcoll1(self.m_urns, self.n_balls, c) for c in range(self.n_balls - 1)
            ]
            ecdf = EcdfFromAccumulatedProbability(ar)
            return ecdf

    class __NullHypothesisHelper:

        def __init__(self, segments: int, dimensions: int):
            self.m_urns = segments ** dimensions
            self.dimensions = dimensions
            self.segments = segments

        def test(self, data: typing.List[int], significance_level: float):
            # Ball is a self.dimensions-dimensional vector.
            self.n_balls = len(data) // self.dimensions
            c_collisions = self.get_collisions(data)
            print(f"{c_collisions=}")
            # pdb.set_trace()
            g = CollisionTest.StatisticHelper(
                c_collisions, self.m_urns, self.n_balls, self.dimensions
            )
            test_result = g.test(significance_level)
            return test_result

        def get_collisions(self, data):
            c_collisions = 0
            count = dict()

            def update_count(serie):
                # Encode serie as number in m_urns-ary system.
                index = 0
                for i in range(self.dimensions):
                    index += serie[i] * self.segments ** i
                if index in count:
                    return 1
                else:
                    count[index] = 1
                    return 0

            n = len(data)
            serie_len = self.dimensions
            if n % serie_len != 0:
                n -= n % serie_len
            for i in range(0, n, serie_len):
                serie = tuple(data[i: i + serie_len])
                c_collisions += update_count(serie)

            return c_collisions

    def perform(self, gen: BaseGenerator, DATA_SIZE: int = None):
        # DATA_SIZE must be chosen elaborately and depends on number segments
        # and dimensions. Don't use one from user.
        n_tests = 0
        passed_tests = 0
        for segments, dimensions, n_balls in [
            (10, 2, 50),
            (10, 3, 10 ** 2),
            (10, 5, 10 ** 3),
            (10, 6, 10 ** 4),
            (10, 7, 10 ** 5),
            (2, 8, 2 ** 5),
            (2, 10, 2 ** 8),
            (2, 15, 2 ** 10),
            (2, 20, 2 ** 14),
            (2, 22, 2 ** 15),
        ]:
            dist = UniformIntDistribution(0, segments - 1)
            data = [dist(gen) for i in range(n_balls * dimensions)]
            print("----")
            print(f"{segments=}, {dimensions=}")
            SIGNIFICANCE = 0.05
            s = CollisionTest.__NullHypothesisHelper(segments, dimensions)
            test_result = s.test(data, SIGNIFICANCE)
            passed_tests += test_result.value()
            print("    collision result:", test_result)
            n_tests += 1
        return passed_tests, n_tests

    def __str__(self):
        return "Collision test"

    def weight(self) -> float:
        return 15
