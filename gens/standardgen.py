from .basegenerator import BaseGenerator
import random


class StandardGen(BaseGenerator):

    def min(self):
        return 0

    def max(self):
        return 2 ** 32 - 1

    def __call__(self):
        return random.randint(self.min(), self.max())

    def entropy(self):
        return self.max().bit_length()
