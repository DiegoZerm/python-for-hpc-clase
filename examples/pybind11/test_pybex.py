#!/usr/bin/env python

import numpy as np
from time import time
from pybex import cube


def test_pybex_cube(N=384):
    v = np.full((N, N, N), fill_value=2.0)

    # (1) compute the result using our C extension
    t0 = time()
    w_ext = cube(v)
    dt0 = time() - t0

    # (2) compute the result using NumPy, note the relative inefficiency
    t0 = time()
    w_ref = v * v * v
    dt1 = time() - t0

    # (3) compare both the results, be careful with NumPy temporary arrays
    try:
        assert(np.allclose(w_ext, w_ref))
        #assert(np.allclose(w_ext[-1,-1,-1], w_ref[-1,-1,-1]))
    except:
        raise
    else:
        print("OK! t(C)=%f, t(NumPy)=%f" % (dt0, dt1))


if __name__ == "__main__":
    test_pybex_cube()

