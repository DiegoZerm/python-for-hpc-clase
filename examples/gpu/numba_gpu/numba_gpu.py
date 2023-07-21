#!/usr/bin/env python3
# Numba CUDA example
import numpy as np
from numba import cuda

@cuda.jit
def increment_by_one(a):
    # thread id, blocks, are the same as in native CUDA
    tx = cuda.threadIdx.x
    ty = cuda.blockIdx.x
    bw = cuda.blockDim.x
    i = tx + ty * bw
    if i < a.size:  # check array boundaries
        a[i] += 1

# set up input array and expected output
x = np.arange(2**20, dtype=np.int32)
y = x + 1

# set up kernel launch configuration
threadsperblock = 32
blockspergrid = (x.size + (threadsperblock - 1)) // threadsperblock

# run kernel
increment_by_one[blockspergrid, threadsperblock](x)

# check result
assert(all(x==y))
print("OK!")
