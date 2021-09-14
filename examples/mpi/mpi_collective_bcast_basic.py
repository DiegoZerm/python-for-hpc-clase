#!/usr/bin/env python3
# mpi_collective_bcast_basic.py
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'key1' : [7, 2.72, 2+3j],
            'key2' : ('abc', 'xyz')}
else:
    data = None

# broadcast the data from rank 0 to all the other ranks
data = comm.bcast(data, root=0)

if rank > 0:
    print("Hello from rank "+str(rank)+". I received: data=" + str(data))
