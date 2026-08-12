"""Placeholder decoder logic.

Replace this with the real model. It exists so the package imports cleanly,
the test suite has something to assert on, and your editor has a typed symbol
to demonstrate go-to-definition and hover against.
"""

from collections.abc import Sequence

import numpy as np


def syndrome_weight(syndrome: Sequence[int]) -> int:
    """Return the Hamming weight of a syndrome bitstring.

    The number of triggered stabilizer measurements -- the simplest possible
    signal a decoder can act on.
    """
    return int(np.count_nonzero(np.asarray(syndrome)))
