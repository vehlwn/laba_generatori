from .basegenerator import BaseGenerator
import pdb


class BitsEngine:

    def __call__(self, gen: BaseGenerator, w: int):
        """Returns integer with up to w significant bits [0..2**w).
        """
        gen_min = gen.min()
        gen_width = gen.entropy()
        mask = (1 << gen_width) - 1
        n_steps = (w + gen_width - 1) // gen_width
        ret = 0
        for i in range(n_steps):
            u = gen() - gen_min
            v = u & mask
            ret = (ret << gen_width) + v
        # Take higher w bits.
        generated_bits = n_steps * gen_width
        ret >>= generated_bits - w
        return ret
