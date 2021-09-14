#!/usr/bin/env python3
from mpi4py import MPI
import numpy as np
from time import sleep


def load_data(index):
    return np.arange(N) * 1000 * index


def compute_something_difficult(data, wait=True):
    if wait:
        sleep(1)
    return np.sum(1.0/np.sqrt((data + 10.0)**2))


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
number_ranks = comm.Get_size()

N = 20

indices = np.arange(N)
results = np.zeros_like(indices, dtype=np.float64)

local_selection = indices % number_ranks == rank
for index in indices[local_selection]:
    print("Rank {} working on index {}.".format(rank, index))
    data = load_data(index)
    results[index] = compute_something_difficult(data)

results_sum = np.zeros_like(results)
comm.Allreduce(results, results_sum, op=MPI.SUM)
results = results_sum

results_expected = [compute_something_difficult(load_data(index), wait=False)
                    for index in indices]
print("Results valid: {} on rank {}.".format(
    np.allclose(results, results_expected), rank))
