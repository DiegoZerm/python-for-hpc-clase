import numpy as np
from corr import velcorr


def velcorrelation_cython(pos, vel, real_edges, nbins):
    npart = pos.shape[0]
    numbers_todo = np.arange(npart)
    rank = 0
    
    # call cython function
    sumcorr, numbin = velcorr(numbers_todo, pos, vel, real_edges, nbins, rank)
    
    return sumcorr, numbin
