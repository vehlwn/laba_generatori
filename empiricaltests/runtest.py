from ..gens.basegenerator import BaseGenerator
from ..nullhypothesis import NullHypothesisChi2
from ..uniformdist import UniformRealDistribution
from .baseempiricaltest import BaseEmpiricalTest
import math
import pdb
import typing


class RunTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, G. Run test, pp 66.
    """

    class Chi2Statistic(NullHypothesisChi2):

        def __init__(self, count: typing.List[int], n: int):
            super().__init__()
            super().set_v(6)
            self.count = count
            self.n = n

        def statistic(self):
            # Bad matrix.
            A = [
                [4529.4, 9044.9, 13568, 18091, 22615, 27892],
                [9044.9, 18097, 27139, 36187, 45234, 55789],
                [13568, 27139, 40721, 54281, 67852, 83685],
                [18091, 36187, 54281, 72414, 90470, 111580],
                [22615, 45234, 67852, 90470, 113262, 139476],
                [27892, 55789, 83685, 111580, 139476, 172860],
            ]
            V = 0
            # Morgan, Byron J. T - Elements of Simulation-Chapman & Hall_CRC
            # (2018), 6: Testing Random Numbers, 6.4 Runs tests, pp 144.
            expected = [
                (k ** 2 + k - 1) / math.factorial(k + 2) * (self.n - k - 1)
                for k in range(1, 6 + 1)
            ]
            print(f"{expected=}")
            for i in range(6):
                for j in range(6):
                    V += (
                        (self.count[i] - expected[i])
                        * (self.count[j] - expected[j])
                        * A[i][j]
                    ) / self.n
            return V

    class __NullHypothesisHelper:

        def __init__(self, runs_up: bool):
            self.__runs_up = runs_up

        def test(self, data, significance_level):
            count = self.get_count_runs(data)
            print(f"{count=}")
            g = RunTest.Chi2Statistic(count, len(data))
            test_result = g.test(significance_level)
            return test_result

        def get_count_runs(self, data):
            n = len(data)
            count = [0] * 6

            def update_count(run_len):
                if run_len >= 6:
                    count[5] += 1
                else:
                    count[run_len - 1] += 1

            run_start = 0
            for i in range(1, n):
                if (
                    self.__runs_up
                    and data[i] < data[i - 1]
                    or not self.__runs_up
                    and data[i - 1] < data[i]
                ):
                    run_len = i - run_start
                    update_count(run_len)
                    run_start = i
            # Last run.
            run_len = n - run_start
            update_count(run_len)

            return count

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 2
        passed_tests = 0
        dist = UniformRealDistribution(0.0, 1.0)
        # dist = UniformIntDistribution(0, 9)
        data = [dist(gen) for i in range(DATA_SIZE)]

        print("----")
        print("Runs up")
        SIGNIFICANCE = 0.05
        s = RunTest.__NullHypothesisHelper(True)
        test_result = s.test(data, SIGNIFICANCE)
        passed_tests += test_result.value()
        print("    chi2:", test_result)

        print("----")
        print("Runs down")
        s = RunTest.__NullHypothesisHelper(False)
        test_result = s.test(data, SIGNIFICANCE)
        passed_tests += test_result.value()
        print("    chi2:", test_result)

        return passed_tests, n_tests

    def __str__(self):
        return "Run test"

    def weight(self) -> float:
        return 10
