from empiricaltests.birthdayspacingtest import BirthdaySpacingTest
from empiricaltests.collisiontest import CollisionTest
from empiricaltests.frequencytest import FrequencyTest
from empiricaltests.gaptest import GapTest
from empiricaltests.maximumofttest import MaximumOfTTest
from empiricaltests.permutationtest import PermutationTest
from empiricaltests.pokertest import PockerTest
from empiricaltests.runtest2 import RunTest2
from empiricaltests.serialcorrelationtest import SerialCorrelationTest
from empiricaltests.serialtest import SerialTest
from gens.laggedfibgen import LaggedFibGen
from gens.linearcongruentialgen import Lcg
from gens.randomizbyshuffl import RandomizeByShuffleM, RandomizeByShuffleB
from gens.standardgen import StandardGen
import random


DATA_SIZE = 10_000
seed = random.randint(0, 2 ** 32 - 1)
# gen = RandomizeByShuffleM(Lcg(seed), LaggedFibGen(seed), k=3000)
# gen = RandomizeByShuffleB(Lcg(seed), k=3000)
gen = Lcg(seed)
# gen = LaggedFibGen(seed)
# gen = StandardGen()


total_passed_tests = 0.0
total_tests = 0.0
for test in [
    FrequencyTest(),
    SerialTest(),
    PermutationTest(),
    SerialCorrelationTest(),
    PockerTest(),
    MaximumOfTTest(),
    GapTest(),
    RunTest2(),
    CollisionTest(),
    BirthdaySpacingTest(),
]:
    print("--------\n" + str(test) + ": ")
    (passed_tests, n_tests) = test.perform(gen, DATA_SIZE)
    print(f"Passed {passed_tests}/{n_tests} {str(test)}")
    total_passed_tests += passed_tests * test.weight()
    total_tests += n_tests * test.weight()

print(
    f"Total passed {total_passed_tests}/{total_tests} tests"
    f" ({total_passed_tests/total_tests*100.:.3g} %)"
)
