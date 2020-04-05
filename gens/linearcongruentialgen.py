from .basegenerator import BaseGenerator


class Lcg(BaseGenerator):
    """X_n = (a * X_{n-1} + c) mod m, m = 2**e
    i) c is relatively prime to m;
    ii) b=a-1 is multiple of p for every prime factors of m;
    iii) b is multiple of 4, if m is multiple of 4.
    a and c can be 0 <= a < m, 0 <= c <= m.
    For example, if m=2**e, c must be odd, a-1 must be multiple of 4:
    a           c            m = 2**32
    1222555645, 2926597579,
    3132807169, 2464122885,
    3526140793, 2711318523,
    3530751989, 4043425385,
    3544340349, 2652960205,

                             m = 2**64
    11947160550052370021, 834415620950361107
    12355867657523950689, 12510077294470928589
    13230239459315600573, 2939572128185299857
    14804111965209366173, 3675177112584906757
    15299833934436520945, 16066170322407132827
    16182325404058577641, 3387312685192749113
    16249977706766770345, 12348638665728963797
    16821832941845169513, 13402225554297672833
    4903171292778976825, 7692654931372905407
    8772493171407494373, 16870534210670311047
    """

    def __init__(
        self, seed: int = 0, a: int = 3544340349, c: int = 2652960205, m: int = 2 ** 32
    ):
        super().__init__()
        self.__state = seed
        self.__a = a
        self.__c = c
        self.__m = m

    def min(self) -> int:
        return 0

    def max(self) -> int:
        return self.__m - 1

    def __call__(self) -> int:
        self.__state = (self.__state * self.__a + self.__c) % self.__m
        return self.__state

    def entropy(self) -> int:
        ret = self.max().bit_length()
        if (1 << ret) - 1 > self.max():
            ret -= 1
        return ret
