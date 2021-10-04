from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# check that we have only 2 ranks
if size != 2:
    if rank == 0:
        print("Wrong number of ranks! Works only with 2 ranks.")
        sys.stdout.flush()
    comm.Barrier()
    comm.Abort()

if rank == 0:
    # start sending on rank 0
    for i in range(10):
        comm.send(i, dest=1)
        data = comm.recv(source=1)
        print("Rank {:d} received {:d}.".format(rank, data))
else:
    # start receiving on rank 1
    for i in range(100, 110):
        data = comm.recv(source=0)
        print("Rank {:d} received {:d}.".format(rank, data))
        comm.send(i, dest=0)
