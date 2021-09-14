#!/usr/bin/env python3
# mpi_point_to_point_numpy.py
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n_elem = 4

# automatic MPI datatype discovery
if rank == 0:
    data = np.arange(n_elem, dtype=np.float64)
    comm.Send(data, dest=1, tag=13)
elif rank == 1:
    data = np.empty(n_elem, dtype=np.float64)
    comm.Recv(data, source=0, tag=13)
    print("Hello from rank 1. I received: data="+str(data))
