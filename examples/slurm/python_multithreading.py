#!/usr/bin/env python

import numpy as np

n = 4096
M = np.random.rand(n, n)

# The following call may use multi-threading using the underlying
# high-performance math libraries NumPy is linked to (e.g. MKL):
N = np.matmul(M, M)

print(N.size)

