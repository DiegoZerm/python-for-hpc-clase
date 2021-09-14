from corr import velcorr
import numpy as np


def am_i_root(run_mpi):
    if not run_mpi:
        return True
    try:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        return rank == 0
    except:
        return True


def broadcast(vel, pos):
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    vel = comm.bcast(vel, root=0)
    pos = comm.bcast(pos, root=0)
    return vel, pos


def wait():
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    comm.Barrier()


def velcorrelation_mpi(pos, vel, real_edges, nbins):
    from mpi4py import MPI
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # static load distribution
    numbers = np.arange(pos.shape[0])
    indices = np.mod(numbers, size) == rank
    numbers_todo = numbers[indices]
    
    # call cython function
    sumcorr, numbin = velcorr(numbers_todo, pos, vel, real_edges, nbins, rank)
    
    # reduce result to root
    comm.Barrier()
    #sumcorr_res = comm.reduce(sumcorr, root=0)
    #numbin_res = comm.reduce(numbin, root=0)
    sumcorr_res = comm.allreduce(sumcorr)
    numbin_res = comm.allreduce(numbin)
    
    return sumcorr_res, numbin_res
