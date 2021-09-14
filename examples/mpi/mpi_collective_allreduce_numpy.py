#!/usr/bin/env python3
# mpi_collective_allreduce_numpy.py
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

data = np.arange(100, dtype=np.float64) + rank * 1000

maximum = data.max()

global_maximum = comm.allreduce(maximum, op=MPI.MAX)

print("Maximum is {} on process {} (global: {}).".format(
    maximum, rank, global_maximum))

data_sum = np.zeros_like(data)
comm.Allreduce(data, data_sum, op=MPI.SUM)


print("Sum of element 50 is {} on process {} (local value: {}).".format(
    data_sum[50], rank, data[50]))
