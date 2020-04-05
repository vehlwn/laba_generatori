class BaseGenerator:
    """Interface for all generators compatible with Uniforn Int, Real Distribution
    and empirical tests.
    """

    def min(self) -> int:
        raise NotImplementedError

    def max(self) -> int:
        raise NotImplementedError

    def __call__(self) -> int:
        raise NotImplementedError

    def entropy(self) -> int:
        raise NotImplementedError
