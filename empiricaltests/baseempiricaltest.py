from gens.basegenerator import BaseGenerator
import typing


class BaseEmpiricalTest:

    def perform(self, gen: BaseGenerator, DATA_SIZE: int) -> typing.Tuple[int, int]:
        """Takes a generator, perform tests and returns pair
        (number_passed_tests, number_all_tests).
        """
        raise NotImplementedError

    def weight(self) -> float:
        """Power of a test.
        """
        raise NotImplementedError
