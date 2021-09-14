import numpy as np
from numpy import linalg as LA
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import h5py


def normalize(sumcorr, numbin, nbins):
    for ind in range(nbins):
        for j in range(6):
            if numbin[ind] > 0:
                sumcorr[ind,j] /= numbin[ind]
    return sumcorr


def plot_correlation(sumcorr, numbin, nbins, minr, maxr, bin_edges, vel):
    sumcorr = normalize(sumcorr, numbin, nbins)
    
    # compute eigenvalues
    A = np.zeros((nbins,3,3))
    A[:,0,0] = sumcorr[:,0]
    A[:,1,1] = sumcorr[:,1]
    A[:,2,2] = sumcorr[:,2]
    A[:,0,1] = A[:,1,0] = sumcorr[:,3]
    A[:,0,2] = A[:,2,0] = sumcorr[:,4]
    A[:,1,2] = A[:,2,1] = sumcorr[:,5]
    vals = np.array([LA.eigvals(A[i]) for i in range(nbins)])

    # save stuff
    with h5py.File('output.hdf5', 'w') as f:
        f['corr'] = sumcorr
        f['numbin'] = numbin
        f['eigvals'] = vals
        f['minr'] = minr
        f['maxr'] = maxr
        f['nbins'] = nbins
        f['bin_edges'] = bin_edges
        f['A'] = A
        f['vmean'] = np.array([vel[:,0].mean(), vel[:,1].mean(), vel[:,2].mean()])
    
    width = 10
    f = plt.figure(figsize=(width,0.6*width))
    labels = ['xx', 'yy', 'zz', 'xy', 'xz', 'yz']
    midpoints = 10**(0.5 * (bin_edges[1:] + bin_edges[:-1]))
    for i in range(6):
        plt.step(midpoints, sumcorr[:,i], where='mid', label=labels[i])
    plt.step(midpoints, sumcorr[:,:3].sum(axis=1), where='mid', label='trace')
    plt.xscale('log')
    plt.xlabel('r')
    plt.legend()
    plt.savefig("plots/corr.pdf")
    plt.close(f)
    f = plt.figure(figsize=(width,0.5*width*3))
    plt.subplot(311)
    plt.step(midpoints, vals[:,0], where='mid')
    plt.xscale('log')
    plt.subplot(312)
    plt.step(midpoints, vals[:,1], where='mid')
    plt.xscale('log')
    plt.subplot(313)
    plt.step(midpoints, vals[:,2], where='mid')
    plt.xscale('log')
    plt.xlabel('r')
    plt.savefig("plots/eig.pdf")
