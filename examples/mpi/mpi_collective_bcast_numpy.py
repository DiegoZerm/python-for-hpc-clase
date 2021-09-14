#!/usr/bin/env python3
# mpi_collective_bcast_numpy.py
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = np.arange(100, dtype=np.int)
else:
    data = np.empty(100, dtype=np.int)

comm.Bcast(data, root=0)

for i in range(100):
    assert data[i] == i
