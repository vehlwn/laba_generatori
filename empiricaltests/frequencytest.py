from .baseempiricaltest import BaseEmpiricalTest
from gens.basegenerator import BaseGenerator
from nullhypothesis import NullHypothesisChi2, NullHypothesisKolm
from numericaldist import EcdfFromUnsortedData
from theordist import cdf_theor_uniform
from uniformdist import UniformRealDistribution


class FrequencyTest(BaseEmpiricalTest):
    """ Knuth, vol 2, par 3.3.2 Empirical Tests, A. Equidistribution test
    (frequency test), pp 61.
    """

    def perform(self, gen: BaseGenerator, DATA_SIZE):
        theor_cdf = lambda x: cdf_theor_uniform(x, 0.0, 1.0)
        dist = UniformRealDistribution(0, 1)
        data = [dist(gen) for i in range(DATA_SIZE)]
        test_desc = [
            ("Whole data:", data),
            ("First half:", data[: DATA_SIZE // 2]),
            ("Last half:", data[DATA_SIZE // 2:]),
            ("Every 2nd:", data[::2]),
            ("Every 3rd:", data[::3]),
            ("Every 5th:", data[::5]),
            ("Every 7th:", data[::7]),
        ]

        def frequency_test_impl(data):
            SIGNIFICANCE = 0.05
            ecdf = EcdfFromUnsortedData(data)
            v = 15
            ret = 0
            g = NullHypothesisChi2()
            g.set_ecdf(ecdf)
            g.set_cdfTheor(theor_cdf)
            g.set_v(v)
            test_result = g.test(SIGNIFICANCE)
            ret += test_result.value()
            print("    chi2:", test_result)

            g = NullHypothesisKolm(ecdf, theor_cdf)
            test_result = g.test(SIGNIFICANCE)
            ret += test_result.value()
            print("    kolm:", test_result)
            return ret

        n_tests = len(test_desc) * 2
        passed_tests = 0
        for s, ar in test_desc:
            print("----\n" + s)
            passed_tests += frequency_test_impl(ar)
        return passed_tests, n_tests

    def __str__(self):
        return "Frequency test"

    def weight(self) -> float:
        return 0.25
