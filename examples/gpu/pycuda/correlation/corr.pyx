#!/usr/bin/python
# coding: utf-8
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt

# define datatypes
ITYPE = np.int
ctypedef np.int_t ITYPE_t

LTYPE = np.int64
ctypedef np.int64_t LTYPE_t

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

# compute velocity correlation for given cell k
@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def velcorr(np.ndarray[ITYPE_t, ndim=1] indices, np.ndarray[DTYPE_t, ndim=2] pos, np.ndarray[DTYPE_t, ndim=2] vel, np.ndarray[DTYPE_t, ndim=1] real_edges, int nbins, int rank):
    cdef DTYPE_t dist, dx, dy, dz
    cdef unsigned int j, i, ind, k 
    cdef DTYPE_t startglob
    cdef np.ndarray[DTYPE_t, ndim=2] velcorr = np.zeros((nbins,6), dtype=DTYPE)
    cdef np.ndarray[LTYPE_t] numbin = np.zeros(nbins, dtype=LTYPE)
    # loop over given cell indices
    for k in indices:
        # loop over particles with index smaller than k
        for j in xrange(k):
            dx = pos[j,0] - pos[k,0]
            dy = pos[j,1] - pos[k,1]
            dz = pos[j,2] - pos[k,2]

            dist = sqrt(dx*dx + dy*dy + dz*dz)
            
            ind = 0
            # loop over radial bins
            for i in xrange(nbins - 1):
                if dist < real_edges[(i+1)]:
                  ind = i+1
                  break
            # compute velocity correlation
            numbin[ind] += 1
            velcorr[ind,0] += vel[k,0] * vel[j,0]
            velcorr[ind,1] += vel[k,1] * vel[j,1]
            velcorr[ind,2] += vel[k,2] * vel[j,2]
            velcorr[ind,3] += vel[k,0] * vel[j,1]
            velcorr[ind,4] += vel[k,0] * vel[j,2]
            velcorr[ind,5] += vel[k,1] * vel[j,2]

    return velcorr, numbin
