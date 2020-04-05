from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2
from uniformdist import UniformRealDistribution
import math
import pdb
import typing


class RunTest2(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, G. Run test, pp 66 (ex 14).
    """

    class Chi2Statistic(NullHypothesisChi2):

        def __init__(self, count: typing.List[int]):
            super().__init__()
            super().set_v(len(count) - 1)
            self.total = sum(count)
            self.p_emp = [x / self.total for x in count]

        def statistic(self):
            expected = [
                1.0 / math.factorial(r) - 1.0 / math.factorial(r + 1)
                for r in range(1, 5 + 1)
            ] + [1.0 / math.factorial(len(self.p_emp))]

            print(f"expected={list(x * self.total for x in expected)}")
            # print(f"expected={expected}")
            # print(f"p_emp={self.p_emp}")
            s = 0.0
            for i in range(len(self.p_emp)):
                s += self.total * \
                    (self.p_emp[i] - expected[i]) ** 2 / expected[i]
            return s

    class __NullHypothesisHelper:

        def __init__(self, runs_up: bool):
            self.__runs_up = runs_up

        def test(self, data, significance_level):
            count = self.get_count_runs(data)
            print(f"{count=}")
            g = RunTest2.Chi2Statistic(count)
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
            i = 1
            while i < n:
                if (
                    self.__runs_up
                    and data[i] < data[i - 1]
                    or not self.__runs_up
                    and data[i - 1] < data[i]
                ):
                    run_len = i - run_start
                    update_count(run_len)
                    # Throw away the element immediately following a run.
                    i += 1
                    run_start = i
                i += 1
            # Last run.
            run_len = n - run_start
            if run_len:
                update_count(run_len)

            return count

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 2
        passed_tests = 0
        dist = UniformRealDistribution(0.0, 1.0)
        data = [dist(gen) for i in range(DATA_SIZE)]

        print("----")
        print("Runs up")
        SIGNIFICANCE = 0.05
        s = RunTest2.__NullHypothesisHelper(True)
        test_result = s.test(data, SIGNIFICANCE)
        passed_tests += test_result.value()
        print("    chi2:", test_result)

        print("----")
        print("Runs down")
        s = RunTest2.__NullHypothesisHelper(False)
        test_result = s.test(data, SIGNIFICANCE)
        passed_tests += test_result.value()
        print("    chi2:", test_result)

        return passed_tests, n_tests

    def __str__(self):
        return "Run test"

    def weight(self) -> float:
        return 10
