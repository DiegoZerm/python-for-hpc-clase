#!/usr/bin/env python3

"""
fft_scipy_cupy_jax.py

Usage demo and performance comparison of the FFTs provided by

* SciPy (CPU, backend depends on the installation and could be internal, MKL, FFTW, etc.)
* CuPy (GPU)
* JAX (GPU, fallback to CPU)

Part of the MPCDF Python for HPC course.
"""

import os
import numpy as np
import scipy
from time import time

use_pyfftw=False
if use_pyfftw:
    import pyfftw

use_cupy=True
if use_cupy:
    import cupy as cp
    import cupyx.scipy.fft as cufft

use_jax=True
if use_jax:
    import jax
    import jax.numpy as jnp
    # in case double precision is required, JAX expects you to enable this explicitly
    jax.config.update("jax_enable_x64", True)


# --- size and number of timed iterations ---
n_elem = 2**28
n_iter = 3


# --- set up double complex input array ---
a = np.random.uniform(-1., 1., n_elem) + 1.j * np.random.uniform(-1., 1., n_elem)
a_gb = a.size * a.itemsize / 2**30
print(f"FFT input array size: {a_gb} GiB")


# --- CPU, SciPy default ---
# warmup
b = scipy.fft.fft(a)
# measure
t0 = time()
for i in range(n_iter):
    b = scipy.fft.fft(a)
dt = (time() - t0)/n_iter
print(f"SciPy: {dt} s")


# --- CPU, SciPy FFTW backend, can sometimes be faster than the default ---
if use_pyfftw:
    pyfftw.config.NUM_THREADS = int(os.environ["OMP_NUM_THREADS"])
    with scipy.fft.set_backend(pyfftw.interfaces.scipy_fft):
        pyfftw.interfaces.cache.enable()
        b_fftw = scipy.fft.fft(a)
        t0 = time()
        for i in range(n_iter):
            b_fftw = scipy.fft.fft(a)
        dt = (time() - t0)/n_iter
        print(f"FFTW:  {dt} s")
        assert(np.allclose(b, b_fftw))


# --- GPU, CuPy ---
if use_cupy:
    a_d = cp.asarray(a)
    with scipy.fft.set_backend(cufft):
        b_d = scipy.fft.fft(a_d)
        b_h = cp.asnumpy(b_d)
        t0 = time()
        for i in range(n_iter):
            b_d = scipy.fft.fft(a_d)
        b_h = cp.asnumpy(b_d)
        dt = (time() - t0)/n_iter
        print(f"CuPy:  {dt} s")
        assert(np.allclose(b, b_h))


# --- JAX, GPU (or CPU as a fallback) ---
if use_jax:
    a_d = jax.device_put(a)
    b_j = jnp.fft.fft(a_d).block_until_ready()
    t0 = time()
    for i in range(n_iter-1):
        b_j = jnp.fft.fft(a_d)
    b_j = jnp.fft.fft(a_d).block_until_ready()
    b_h = jax.device_get(b_j)
    dt = (time() - t0)/n_iter
    print(f"JAX:   {dt} s")
    assert(np.allclose(b, b_j))

