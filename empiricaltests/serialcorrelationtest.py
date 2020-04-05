from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import TestResult
from uniformdist import UniformRealDistribution
import math
import numpy
import pdb
import typing


class SerialCorrelationTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, K. Serial correlation test, pp 72.
    """

    class TestResultHelper(TestResult):

        def __init__(
            self,
            significance_level: float,
            reachedS: float,
            crit_s_left: float,
            crit_s_right: float,
        ):
            self.__significance_level = significance_level
            self.__reachedS = reachedS
            self.__crit_s_left = crit_s_left
            self.__crit_s_right = crit_s_right
            self.__left_pvalue = self.__significance_level / 2.0
            self.__right_pvalue = 1.0 - self.__significance_level / 2.0

        def __str__(self):
            ret = ""
            if not self.value():
                ret += (
                    f"Too bad. Reject with probability {1.-self.__significance_level}"
                )
                if self.__reachedS < self.__crit_s_left:
                    ret += f" (reached S < {self.__crit_s_left})"
                else:
                    ret += f" (reached S > {self.__crit_s_right})"
            else:
                ret += (
                    f"Do not reject with probability {1. - self.__significance_level}"
                )
            ret += (
                f"\nleft critical statistic = {self.__crit_s_left} (P = {self.__left_pvalue})"
                f"\nreached statistic = {self.__reachedS}"
                f"\nright critical statistic = {self.__crit_s_right} (P = {self.__right_pvalue})"
            )
            return ret

        def value(self):
            return self.__crit_s_left < self.__reachedS < self.__crit_s_right

    class __NullHypothesisHelper:

        def __init__(self, lag: int):
            self.__lag = lag

        def test(self, data):
            corrcoef = self.get_corrcoef(data)
            print(f"{corrcoef=}")
            n = len(data)
            mu_n = -1.0 / (n - 1.0)
            sigma2_n = n ** 2 / (n - 1.0) ** 2 / (n - 2.0)

            significance_level = 0.05
            reachedS = corrcoef
            crit_s_left = mu_n - 2 * sigma2_n
            crit_s_right = mu_n + 2 * sigma2_n
            test_result = SerialCorrelationTest.TestResultHelper(
                significance_level, reachedS, crit_s_left, crit_s_right
            )
            return test_result

        def get_corrcoef(self, data: typing.List[float]):
            n = len(data)
            data2 = [data[(i + self.__lag) % n] for i in range(n)]
            # For two variables Pearson correlation coefficients matrix is
            # simmetric 2x2 matrix with ones on a principal diagonal.
            return numpy.corrcoef([data, data2])[0][1]

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 0
        passed_tests = 0
        dist = UniformRealDistribution(0.0, 1.0)
        data = [dist(gen) for i in range(DATA_SIZE)]

        for lag in [1, 2, 5, 10, 20]:
            print("----")
            print(f"{lag=}")
            s = SerialCorrelationTest.__NullHypothesisHelper(lag)
            test_result = s.test(data)
            passed_tests += test_result.value()
            print("    chi2:", test_result)
            n_tests += 1

        return passed_tests, n_tests

    def __str__(self):
        return "Serial correlation test"

    def weight(self) -> float:
        return 1
