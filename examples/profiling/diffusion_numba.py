#!/usr/bin/env python

# --- exported from Diffusion.ipynb ---


import numpy as np
from numba import jit, njit

# parameters (global, for convenience)
n_iterations = 10
n_points = 512
dt = 0.12
D = 1.2


# provide a stub for '@profile' in case line_profiler is not used
import builtins
try:
    builtins.profile
except AttributeError:
    def profile(func):
        return func
    builtins.profile = profile


def init(val=0.5):
    """Set up a 2d NumPy array with some local square initial value pattern."""
    grid = np.zeros([n_points+2, n_points+2])
    # set a square patch near the corner to val > 0
    block_lo = int(n_points * .01)
    block_hi = int(n_points * .5)
    grid[block_lo:block_hi, block_lo:block_hi] = val
    return grid


def main_loop(evolve_func, grid):
    """Main loop function, calling evolve_func on grid."""
    grid_tmp = np.empty_like(grid)
    for i in range(1, n_iterations+1):
        apply_periodic_bc_python(grid, n_points)
        evolve_func(grid, grid_tmp, n_points, dt, D)
        # swap references, do not copy
        if grid_tmp is not None:
            grid_foo = grid
            grid = grid_tmp
            grid_tmp = grid_foo
    return grid


@njit()
def apply_periodic_bc_python(grid, n_points):
    """Explicitly apply periodic boundary conditions, via Python loops."""
    for j in range(n_points + 2):
        grid[ 0, j] = grid[-2, j]
        grid[-1, j] = grid[ 1, j]
    for i in range(n_points + 2):
        grid[ i,-1] = grid[ i, 1]
        grid[ i, 0] = grid[ i,-2]


@njit
def evolve_python(grid, grid_tmp, n_points, dt, D):
    for i in range(1, n_points+1):
        for j in range(1, n_points+1):
            # stencil formula
            grid_tmp[i, j] = grid[i, j] + dt * D * (
                grid[i-1, j] + grid[i+1, j] + grid[i, j-1] + grid[i, j+1]
                - 4.0 * grid[i, j])


grid = init()
solution_python = main_loop(evolve_python, grid)

