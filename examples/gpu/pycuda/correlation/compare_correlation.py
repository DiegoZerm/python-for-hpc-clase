#!/usr/bin/env python3
# coding: utf-8
import sys
import os
import time
import numpy as np
import h5py

from correlation_cython import velcorrelation_cython
from correlation_gpu import velcorrelation_gpu
from correlation_mpi import velcorrelation_mpi, am_i_root, broadcast, wait
from correlation_python import velcorrelation_v1, velcorrelation_v2
from plot_correlation import plot_correlation

run_mpi = True
run_gpu = True
run_cython = True
run_python = False
debug = False

if am_i_root(run_mpi):
    if not os.path.exists('plots/'):
        os.mkdir('plots/')

    # read positions and velocities
    with h5py.File('data.hdf5', 'r') as f:
        vel = f['vel'][:]
        pos = f['pos'][:]
else:
    vel = None
    pos = None

if run_mpi:
    vel, pos = broadcast(vel, pos)

# number of cells as first argument
if len(sys.argv) > 1:
    number = int(sys.argv[1])
else:
    number = 1000

vel = vel[:number,:]
pos = pos[:number,:]

nbins = 50
minr = np.log10(1e9) 
maxr = np.log10(7e12)
real_edges = np.logspace(minr, maxr, nbins+1)
bin_edges = np.log10(real_edges)
npart = pos.shape[0]

if run_gpu:
    if am_i_root(run_mpi):
        print("starting gpu processing.")
        start = time.clock()
        sumcorr, numbin = velcorrelation_gpu(pos, vel, real_edges, nbins)
        end = time.clock()
        print("gpu took ", end - start, " s")
        if debug:
            print("total number of pairs: {:d}, gpu: {:d}"
                  .format(npart*(npart-1)//2, int(numbin.sum())))
        sys.stdout.flush()

if run_cython:
    print("starting cython processing.")
    start = time.clock()
    sumcorr, numbin = velcorrelation_cython(pos, vel, real_edges, nbins)
    end = time.clock()
    print("cython took ", end - start, " s")
    if debug:
        print("total number of pairs: {:d}, cython: {:d}"
              .format(npart*(npart-1)//2, int(numbin.sum())))
    sys.stdout.flush()

if run_python:
    print("starting python v1 processing.")
    start = time.clock()
    sumcorr, numbin = velcorrelation_v1(pos, vel, real_edges, nbins)
    end = time.clock()
    print("python v1 took ", end - start, " s")
    if debug:
        print("total number of pairs: {:d}, python: {:d}"
              .format(npart*(npart-1)//2, int(numbin.sum())))
    sys.stdout.flush()

    print("starting python v2 processing.")
    start = time.clock()
    sumcorr, numbin = velcorrelation_v2(pos, vel, real_edges, nbins)
    end = time.clock()
    print("python v2 took ", end - start, " s")
    if debug:
        print("total number of pairs: {:d}, python: {:d}"
              .format(npart*(npart-1)//2, int(numbin.sum())))
    sys.stdout.flush()

if run_mpi:
    wait()
    print("starting mpi processing.")
    start = time.clock()
    sumcorr, numbin = velcorrelation_mpi(pos, vel, real_edges, nbins)
    end = time.clock()
    print("mpi took ", end - start, " s")
    if debug:
        print("total number of pairs: {:d}, mpi: {:d}"
              .format(npart*(npart-1)//2, int(numbin.sum())))
    sys.stdout.flush()


if am_i_root(run_mpi):
    plot_correlation(sumcorr, numbin, nbins, minr, maxr, bin_edges, vel)
