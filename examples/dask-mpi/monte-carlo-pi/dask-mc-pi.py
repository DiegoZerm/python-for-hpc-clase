# basic parameters
n_darts = 2**20
n_tasks = 32
# visualization unfortunately fails on Raven due to missing fonts on the compute nodes
visualize_graph = False
# set to True when running via dask_mpi, otherwise a LocalCluster() is used
use_mpi = False


import os, sys
import time
import numpy as np
if use_mpi:
    import dask_mpi as dm
    import dask.distributed as dd
from dask import delayed


def pi_kernel(n_darts, task_number=0, verbose=False):
    """NumPy-based Monte Carlo PI approximation, using n_darts samples.
	"""
    if verbose:
        print(f"task {task_number} on worker {os.getpid()}", file=sys.stderr)
    # generate random points on the 2d plane [-1:1,-1:1]
    p = np.random.uniform(low=-1.0, high=1.0, size=(n_darts, 2))
    # check which points lie within the unit circle
    q_within_circle = p[:,0]*p[:,0] + p[:,1]*p[:,1] < 1.0
    # count the number of points within the circle
    n_within_circle = np.sum(q_within_circle)
    # compute the ratio of the #points within the circle to the # of all points
    return 4.0 * float(n_within_circle)/float(n_darts)


# initialize the MPI-based Dask cluster
if use_mpi:
    dm.initialize(
        local_directory=os.getcwd(),
        dashboard=False,
    )
    client = dd.Client()


# submit simple task graph, consisting of n_tasks independent calculations followed by a final averaging operation
pi = delayed(np.average)([
	delayed(pi_kernel)(n_darts, i) for i in range(n_tasks)
])

if visualize_graph:
    pi.visualize(filename="pi-task-graph.svg")

t0 = time.perf_counter()
pi = pi.compute()
t1 = time.perf_counter()

print(f"pi \\approx {pi} ({t1-t0}s)")

