#!/usr/bin/env python3
# monte_carlo_pi.py

"""
A simple Monte Carlo program to approximate the value of PI.

Sequential version, using NumPy.

Algorithm:
 -- area of square with side length a = 2*r :  (1) A_square = 4*r**2
 -- area of inscribed circle with radius r  :  (2) A_circle = pi * r**2
 -- approximation for pi is obtained by dividing equations (1) and (2)
    4 * A_circle/A_square = pi
 -- let's play darts: the probability of hitting the circle is proportional
    to its area, while are guaranteed to hit the square always
"""

import os
import numpy as np

rng_initialized = False

def pi_kernel(n_trials):
    """Monte Carlo PI approximation, using n_trials samples."""
    # initialize the random number generator once with the process ID,
    # of potential importance when we perform parallel computations
    global rng_initialized
    if not rng_initialized:
        random_seed = os.getpid()
        np.random.seed(random_seed)
        rng_initialized = True
    # generate random points on the 2d plane [-1:1,-1:1]
    p = np.random.uniform(low=-1.0, high=1.0, size=(n_trials, 2))
    # check which points lie within the unit circle
    q_within_circle = p[:,0]*p[:,0] + p[:,1]*p[:,1] < 1.0
    # count the number of points within the circle
    n_within_circle = np.sum(q_within_circle)
    # compute the ratio of the #points within the circle to the # of all the points
    return 4.0 * float(n_within_circle)/float(n_trials)


def approximate_pi(n_samples):
    """Wrapper to call pi_kernel() on batches of 1 Million elements, in order
    to save memory with very large sample numbers."""
    my_pi = 0.0
    batch_size = 2**20  # 1 million elements
    n_remain = n_samples
    while (n_remain > batch_size):
        weight = float(batch_size)/float(n_samples)
        my_pi += weight * pi_kernel(batch_size)
        n_remain -= batch_size
    if n_remain > 0:
        weight = float(n_remain)/float(n_samples)
        my_pi += weight * pi_kernel(n_remain)
    return my_pi


# only run the code when this module is run as the main program,
# not when it is imported
if __name__ == "__main__":
    my_pi = approximate_pi(2**25)
    print("PI deviation = %f" % ( np.abs(my_pi - np.pi)/np.pi ))

