from gens.laggedfibgen import LaggedFibGen
from gens.linearcongruentialgen import Lcg
from gens.randomizbyshuffl import RandomizeByShuffleM, RandomizeByShuffleB
from numericaldist import EmpiricalCdf, EcdfFromUnsortedData
from theordist import cdf_theor_uniform, pdf_theor_uniform
from uniformdist import UniformIntDistribution, UniformRealDistribution
import math
import matplotlib.pyplot as plt
import numpy
import pdb
import random


seed = random.randint(0, 2 ** 32 - 1)
gen = Lcg(seed)
# gen = RandomizeByShuffleM(Lcg(seed), LaggedFibGen(seed))
# gen = RandomizeByShuffleB(Lcg(seed))
# gen = LaggedFibGen(seed)
a = 0
b = 1
dist = UniformRealDistribution(a, b)
data = [dist(gen) for i in range(1_000)]

plot_rows = 2
plot_cols = 2


def plot_emp_theor_cdf(ecdf: EmpiricalCdf, sub_index: int):
    xdata_theor = list(numpy.linspace(a, b))
    ydata_theor = list(map(lambda x: cdf_theor_uniform(x, a, b), xdata_theor))

    xdata_emp = sorted(data)
    ydata_emp = list(map(ecdf, xdata_emp))
    plt.subplot(plot_rows, plot_cols, sub_index)
    plt.plot(xdata_theor, ydata_theor, label="CDF")
    plt.step(xdata_emp, ydata_emp, label="ECDF")
    plt.title("Empirical and theoretical CDF")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.grid(True)


def plot_2d_data(data, sub_index: int):
    xdata = data[0::2]
    ydata = data[1::2]
    plt.subplot(plot_rows, plot_cols, sub_index)
    plt.plot(xdata, ydata, ".")
    plt.title("2D distribution")
    plt.xlabel("x_n")
    plt.ylabel("x_{n+1}")
    plt.grid(True)


def plot_3d_data(data, sub_index: int):
    n = len(data)
    n = n // 3 * 3
    xdata = data[0:n:3]
    ydata = data[1: n + 1: 3]
    zdata = data[2: n + 2: 3]
    print(f"{n=}")
    print(f"{len(xdata)=}, {len(ydata)=}, {len(zdata)=}")

    fig = plt.gcf()
    ax = fig.add_subplot(plot_rows, plot_cols, sub_index, projection="3d")
    ax.scatter(xdata, ydata, zdata, marker=".")
    ax.set_xlabel("x_n")
    ax.set_ylabel("x_{n+1}")
    ax.set_zlabel("x_{n+2}")

    plt.title("3D distribution")
    plt.grid(True)


def plot_pdf(ecdf: EmpiricalCdf, sub_index: int):
    # pdb.set_trace()
    n_bins = int(math.ceil(math.log2(len(data)))) + 1
    xdata_theor = numpy.linspace(a, b, n_bins + 1)
    ydata_theor = list(map(lambda x: pdf_theor_uniform(x, a, b), xdata_theor))

    ydata_emp = []
    d = xdata_theor[1] - xdata_theor[0]
    old_cdf = 0.0
    new_cdf = ecdf(xdata_theor[0])
    for i in range(1, n_bins + 1):
        old_cdf = new_cdf
        new_cdf = ecdf(xdata_theor[i])
        pmf = (new_cdf - old_cdf) / d
        ydata_emp.append(pmf)

    plt.subplot(plot_rows, plot_cols, sub_index)
    # Remove last x point.
    xdata_theor_bar = xdata_theor[:-1]
    plt.bar(
        xdata_theor_bar,
        ydata_emp,
        width=(b - a) / n_bins * 0.7,
        align="edge",
        label="EPDF",
    )
    plt.plot(xdata_theor, ydata_theor, "C1", label="PDF")
    plt.legend()
    plt.title("Empirical and theoretical PDF")
    # plt.ylim(0, theor * 1.5)
    plt.xlabel("x")
    plt.ylabel("f(x)")


ecdf = EcdfFromUnsortedData(data)
sub_index = 0

sub_index += 1
plot_emp_theor_cdf(ecdf, sub_index)

sub_index += 1
plot_pdf(ecdf, sub_index)

sub_index += 1
plot_2d_data(data, sub_index)

sub_index += 1
plot_3d_data(data, sub_index)


plt.show()
