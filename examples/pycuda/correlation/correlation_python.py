import numpy as np

def velcorrelation_v1(pos, vel, real_edges, nbins):
    # return arrays
    velcorr = np.zeros((nbins,6), dtype=np.float64)
    numbin = np.zeros(nbins, dtype=np.int64)
    # loop over all particles
    for k in range(pos.shape[0]):
        dist = np.sqrt(((pos - pos[k][np.newaxis,:])**2).sum(axis=1)) 

        # slow way:
        #bin_indices =  np.array([(dist < real_edges[i+1]) & (dist > real_edges[i]) for i in range(nbins)])
        bin_indices = np.zeros_like(dist)
        indold = dist < real_edges[0]
        # get bins for each distance
        for i, r in enumerate(real_edges[1:]):
            ind = dist < r
            bin_indices[ind & ~indold] = i 
            indold = ind
        # now add up values
        for i in range(nbins):
            in_this_bin = bin_indices == i
            numbin[i] += (in_this_bin).sum()
            velcorr[i, 0] += (vel[k,0] * vel[in_this_bin,0]).sum()
            velcorr[i, 1] += (vel[k,1] * vel[in_this_bin,1]).sum()
            velcorr[i, 2] += (vel[k,2] * vel[in_this_bin,2]).sum()
            velcorr[i, 3] += (vel[k,0] * vel[in_this_bin,1]).sum()
            velcorr[i, 4] += (vel[k,0] * vel[in_this_bin,2]).sum()
            velcorr[i, 5] += (vel[k,1] * vel[in_this_bin,2]).sum()
    return velcorr, numbin


def velcorrelation_v2(pos, vel, real_edges, nbins):
    # return arrays
    velcorr = np.zeros((nbins,6), dtype=np.float64)
    numbin = np.zeros(nbins, dtype=np.int64)
    # loop over given cell indices
    for k in range(pos.shape[0]):
        # loop over particles with index smaller than k
        for j in range(k):
            dx = pos[j,0] - pos[k,0]
            dy = pos[j,1] - pos[k,1]
            dz = pos[j,2] - pos[k,2]

            dist = np.sqrt(dx*dx + dy*dy + dz*dz)
            
            ind = 0
            # loop over radial bins
            for i in range(nbins):
                if dist < real_edges[i+1]:
                  ind = i
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
