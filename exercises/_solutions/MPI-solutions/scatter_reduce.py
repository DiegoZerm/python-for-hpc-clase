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
    print("Average on full data: ", np.mean(data_send))

# empty receive array
data_receive = np.empty(elements_per_rank)

# scatter the data from rank 0
comm.Scatter(data_send, data_receive, root=0)

# compute local average
average = np.mean(data_receive)

# reduce to root as a sum
sum_of_averages = comm.reduce(average, op=MPI.SUM, root=0)

if rank == 0:
    # divide by size
    full_average = sum_of_averages / size

    print("Average on reduced data: ", full_average)
