#!/usr/bin/env python3
# mpi_monte_carlo_pi.py
from mpi4py import MPI
import numpy as np
import monte_carlo_pi as mcp

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# number of Monte Carlo samples per worker process
n_samples = 2**24
# --> the more workers and samples we use the more accurate the approximation gets

# compute an approximation of pi on the current process
pi_local = mcp.approximate_pi(n_samples)

# gather all the results on MPI rank 0 into a list
pi_list = comm.gather(pi_local, root=0)

if rank == 0:
    my_pi = np.average(pi_list)
    print("PI deviation = %f" % ( np.abs(my_pi - np.pi)/np.pi ))
