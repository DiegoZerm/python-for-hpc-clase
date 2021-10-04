from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = {'very': 'nice'}
# start sending on rank 0
if rank == 0:
    comm.send(data, dest=1)

# source is left from current rank
source = rank - 1
# wrap around if < 0
if source < 0:
    source += size
# destination is right from current rank
destination = rank + 1
# wrap around if too large
if destination > size - 1:
    destination -= size

# do several rounds
rounds = 10
for i in range(rounds):
    # receive the data
    data_recv = comm.recv(source=source)
    print("Rank {:d} received {} from rank {:d} in round {:d}.".format(
        rank, data_recv, source, i))
    sys.stdout.flush()
    # now send except for rank 0 in the last round
    if rank != 0 or i < rounds - 1:
        comm.send(data, dest=destination)
