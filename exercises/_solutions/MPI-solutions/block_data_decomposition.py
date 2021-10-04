from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 15

# get block domain decomposition
edges = np.arange(size + 1) * N // size
offsets = edges[:-1]
# sizes on all cores
sizes = np.diff(edges)
# bounds on this core
bounds = (edges[rank], edges[rank+1])

# define the local array
local_array = np.arange(bounds[0], bounds[1], dtype=np.float64)
print("Data on rank {:d}: {}".format(rank, local_array))

data_receive = np.empty(0)
if rank == 0:
    data_receive = np.empty(N)

# now gather this on rank 0
comm.Gatherv([local_array, sizes[rank], MPI.DOUBLE],
             [data_receive, sizes, offsets, MPI.DOUBLE], root=0)

if rank == 0:
    print("Gathered data: {}".format(data_receive))

# modify on rank 0
if rank == 0:
    data_receive *= 10.
    print("Modified data: {}".format(data_receive))

# and scatter it back
comm.Scatterv([data_receive, sizes, offsets, MPI.DOUBLE],
              [local_array, sizes[rank], MPI.DOUBLE], root=0)

# now print on each rank
print("Modified data on rank {:d}: {}".format(rank, local_array))
