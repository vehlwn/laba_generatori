from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisKolm
from numericaldist import EcdfFromUnsortedData
from uniformdist import UniformRealDistribution


class MaximumOfTTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, H. Maximum of t test, pp 70.
    """

    class __NullHypothesisHelper:

        def test(self, data, significance_level, t):
            ecdf = self.get_ecdf_from_series(data, t)
            theor_cdf = lambda x: x ** t
            g = NullHypothesisKolm(ecdf, theor_cdf)
            test_result = g.test(significance_level)
            return test_result

        def get_ecdf_from_series(self, data, t):
            n = len(data)
            if n % t != 0:
                n -= n % t
            v = []
            for i in range(0, n, t):
                serie = data[i: i + t]
                v.append(max(serie))
            ecdf = EcdfFromUnsortedData(v)
            return ecdf

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        n_tests = 0
        passed_tests = 0
        dist = UniformRealDistribution(0.0, 1.0)
        data = [dist(gen) for i in range(DATA_SIZE)]
        for t in range(2, 12):
            print("----")
            print(f"{t=}")
            SIGNIFICANCE = 0.05
            s = MaximumOfTTest.__NullHypothesisHelper()
            test_result = s.test(data, SIGNIFICANCE, t)
            passed_tests += test_result.value()
            print("    kolm:", test_result)
            n_tests += 1
        return passed_tests, n_tests

    def __str__(self):
        return "Maximum of t test"

    def weight(self) -> float:
        return 2
