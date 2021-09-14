#!/usr/bin/env python3
# mpi_point_to_point_basic.py
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    # note: data is packed using 'pickle' internally
    comm.send(data, dest=1, tag=11)
elif rank == 1:
    # note: data is unpacked using 'pickle' internally
    data = comm.recv(source=0, tag=11)
    print("Hello from rank 1. I received: data="+str(data))
