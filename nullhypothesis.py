from distfunctions import invCdf
from numericaldist import EmpiricalCdf, EcdfFromUnsortedData
import math
import numpy
import pdb
import scipy.stats


class TestResult:
    """Result for two sided test.
    """

    def __init__(
        self,
        reachedP: float,
        significance_level: float,
        reachedS: float,
        crit_s_left: float,
        crit_s_right: float,
    ):
        self.__reachedP = reachedP
        self.__significance_level = significance_level
        self.__reachedS = reachedS
        self.__crit_s_left = crit_s_left
        self.__crit_s_right = crit_s_right
        self.__left_pvalue = self.__significance_level / 2.0
        self.__right_pvalue = 1.0 - self.__significance_level / 2.0

    def __str__(self):
        ret = ""
        if self.__reachedP < self.__left_pvalue:
            ret += f"Too good. Reject with probability {1. - self.__significance_level} (reached p < {self.__left_pvalue})"
        elif self.__reachedP > self.__right_pvalue:
            ret += f"Too bad. Reject with probability {1.-self.__significance_level} (reached p > {self.__right_pvalue})"
        else:
            ret += f"Do not reject with probability {1. - self.__significance_level}"
        ret += (
            f"\nleft critical statistic = {self.__crit_s_left} (P = {self.__left_pvalue})"
            f"\nreached statistic = {self.__reachedS} (P = {self.__reachedP})"
            f"\nright critical statistic = {self.__crit_s_right} (P = {self.__right_pvalue})"
        )
        return ret

    def value(self):
        return self.__left_pvalue < self.__reachedP < self.__right_pvalue


class NullHypothesisBase:

    def test(self, significance_level):
        # Calculate statistic for a given ECDF.
        reachedS = self.statistic()
        # Calculate theoretical CDF.
        reachedP = self.cdfStatistic(reachedS)

        def statistic_inv_cdf(x):
            return invCdf(self.cdfStatistic, x)

        crit_s_left = statistic_inv_cdf(significance_level / 2.0)
        crit_s_right = statistic_inv_cdf(1.0 - significance_level / 2.0)
        return TestResult(
            reachedP, significance_level, reachedS, crit_s_left, crit_s_right
        )

    def statistic(self):
        """Empirical statistic.
        """
        raise NotImplementedError()

    def cdfStatistic(self, x):
        """statistic()'s distribution : Chi2 or Kolmogorov.
        """
        raise NotImplementedError()


class NullHypothesisChi2(NullHypothesisBase):
    """Chi2 test.
    """

    def __init__(self):
        super().__init__()

    def set_v(self, v: int):
        """Degrees of freedom.
        """
        self.v = v

    def set_ecdf(self, ecdf: EmpiricalCdf):
        """Empirical data distributiom.
        """
        self.ecdf = ecdf

    def set_cdfTheor(self, cdfTheor):
        """Theoretical data distributiom.
        """
        self.cdfTheor = cdfTheor

    def statistic(self):
        """The Pearson statistic that should have chi2 distribution with v degrees of freedom.
        """
        # Number of intervals.
        k = self.v + 1
        # Split data into k group so that the theoretical probabilities are
        # equal.
        pTheor = 1.0 / k

        # k groups, k + 1 points between them.
        # x intervals are d-quantiles of the cdfTheor.
        Ax = []
        for d in numpy.linspace(0.0, 1.0, k + 1):
            Ax.append(invCdf(self.cdfTheor, d))
        # Relative group hit frequencies are differences between the ecdf.
        pEmp = []
        prev_cdf = 0
        next_cdf = self.ecdf(Ax[0])
        for i in range(k):
            prev_cdf = next_cdf
            next_cdf = self.ecdf(Ax[i + 1])
            pEmp.append(next_cdf - prev_cdf)
        s = 0
        n = self.ecdf.data_size()
        for i in range(k):
            s += n * (pEmp[i] - pTheor) ** 2 / pTheor
        return s

    def cdfStatistic(self, x):
        return scipy.stats.chi2.cdf(x, self.v)


class NullHypothesisKolm(NullHypothesisBase):
    """Kolmogorov-Smirnov test.
    """

    def __init__(self, ecdf: EcdfFromUnsortedData, cdfTheor):
        super().__init__()
        self.ecdf = ecdf
        self.cdfTheor = cdfTheor

    def statistic(self):
        """The Kolmogorov statistic.
        """
        d = -math.inf
        n = len(self.ecdf.sorted_data)
        for i in range(n):
            d1 = (i + 1.0) / n
            d2 = self.cdfTheor(self.ecdf.sorted_data[i])
            d3 = i / n
            d = max([d, d1 - d2, d2 - d3])
        # Bolshev's approximation.
        d = math.sqrt(n) * d + 1.0 / 6.0 / math.sqrt(n)
        return d

    def cdfStatistic(self, x):
        if x <= 0:
            return 0
        return scipy.stats.kstwobign.cdf(x)
