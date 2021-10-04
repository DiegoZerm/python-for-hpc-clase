from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

elements_per_rank = 4

# define data_send on rank 0
data_send = None
if rank == 0:
    data_send = np.arange(elements_per_rank * size, dtype=np.float64)
    print("Data scattered from root: ", data_send)

# empty receive array
data_receive = np.empty(elements_per_rank)

# scatter the data from rank 0
comm.Scatter(data_send, data_receive, root=0)

# print local data
print("Data on rank {:d}: {}".format(rank, data_receive))

# modify local array
data_receive *= 10 ** rank

# gather to root
comm.Gather(data_receive, data_send, root=0)

if rank == 0:
    print("Data gathered on root: ", data_send)
