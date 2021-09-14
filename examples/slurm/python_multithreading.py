#!/usr/bin/env python

import numpy as np

n = 4096
M = np.random.rand(n, n)

# the following call may use threading
N = np.matmul(M, M)

print(N.size)

