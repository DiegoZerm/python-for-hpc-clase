#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print("I am rank {:d} of {:d}.".format(rank, size))
