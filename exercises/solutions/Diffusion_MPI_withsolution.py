#!/usr/bin/env python3
# call with
#    mpiexec -np N python3 Diffusion_MPI.py
# Exercise:
# 1. complete communication of boundaries
# 2. implement gathering the whole grid on rank 0 for plotting (look at Gatherv)
# 3. improve code design
import numpy as np
from mpi4py import MPI
import h5py

# parameters (global, for convenience)
n_iterations = 1000
n_global = 256
n_ghost = 2
dt = 0.12
D = 1.2

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_proc = comm.Get_size()
# get a processor grid that is as square as possible
np_x = int(np.sqrt(n_proc))
while n_proc % np_x != 0:
    np_x -= 1
np_y = n_proc // np_x
# block data decomposition
edges_x = np.arange(np_x+1) * n_global // np_x
sizes_x = np.diff(edges_x)
edges_y = np.arange(np_y+1) * n_global // np_y
sizes_y = np.diff(edges_y)

# communication structure for ghost cell update
cart_neighbors = {}
cart = comm.Create_cart(dims=(np_x, np_y),
                        periods=(True, True), reorder=True)
src, dest = cart.Shift(direction=0, disp=1)
cart_neighbors['left'] = src
cart_neighbors['right'] = dest
src, dest = cart.Shift(direction=1, disp=1)
cart_neighbors['down'] = src
cart_neighbors['up'] = dest

# local array sizes
index_x, index_y = cart.Get_coords(rank)
print("Rank {:d}, indices: {:d},{:d} of grid {:d},{:d}".format(
    rank, index_x, index_y, np_x, np_y))
nx_local = sizes_x[index_x]
ny_local = sizes_y[index_y]
bounds_x = (edges_x[index_x], edges_x[index_x+1])
bounds_y = (edges_y[index_y], edges_y[index_y+1])

def init(val=0.005):
    """Set right a 2d NumPy array with some local square initial value pattern."""
    grid = np.zeros([nx_local+n_ghost, ny_local+n_ghost])
    # set a square patch near the corner to val > 0
    block_lo = int(n_global * .01)
    block_hi = int(n_global * .3)
    indices = np.arange(block_lo, block_hi)
    # only set values if the indices are located on the local processor grid
    for ix in indices:
        if ix < bounds_x[0] or ix > bounds_x[1]:
            continue
        for iy in indices:
            if iy < bounds_y[0] or iy > bounds_y[1]:
                continue
            grid[ix-bounds_x[0], iy-bounds_y[0]] = val

    return grid

def main_loop(evolve_func, grid, grid_tmp=None):
    """Main loop function, calling evolve_func on grid,
    using grid_tmp as scratch array, if necessary."""
    for i in range(1, n_iterations+1):
        evolve_func(grid, grid_tmp)
        # swap references, avoid copy
        if grid_tmp is not None:
            grid_foo = grid
            grid = grid_tmp
            grid_tmp = grid_foo


def apply_periodic_boundary_conditions(grid):
    """Explicitly apply periodic boundary conditions."""
    grid[ 0, :] = grid[-2, :]
    grid[-1, :] = grid[ 1, :]
    grid[ :,-1] = grid[ :, 1]
    grid[ :, 0] = grid[ :,-2]

def apply_periodic_boundary_conditions_mpi(grid):
    """Explicitly apply periodic boundary conditions for MPI case."""
    nx = grid.shape[0] - 2
    ny = grid.shape[1] - 2
    # right
    sendbuf = np.array(grid[nx,1:ny+1])
    recvbuf = np.zeros_like(sendbuf)
    cart.Sendrecv(sendbuf=sendbuf, dest=cart_neighbors['right'],
                  recvbuf=recvbuf, source=cart_neighbors['left'])
    grid[0,1:ny+1] = recvbuf[:]
    # left
    sendbuf = np.array(grid[1,1:ny+1])
    recvbuf = np.zeros_like(sendbuf)
    cart.Sendrecv(sendbuf=sendbuf, dest=cart_neighbors['left'],
                  recvbuf=recvbuf, source=cart_neighbors['right'])
    grid[nx+1,1:ny+1] = recvbuf[:]
    # down
    sendbuf = np.array(grid[1:nx+1,1])
    recvbuf = np.zeros_like(sendbuf)
    cart.Sendrecv(sendbuf=sendbuf, dest=cart_neighbors['down'],
                  recvbuf=recvbuf, source=cart_neighbors['up'])
    grid[1:nx+1,ny+1] = recvbuf[:]
    # up
    sendbuf = np.array(grid[1:nx+1,ny])
    recvbuf = np.zeros_like(sendbuf)
    cart.Sendrecv(sendbuf=sendbuf, dest=cart_neighbors['up'],
                  recvbuf=recvbuf, source=cart_neighbors['down'])
    grid[1:nx+1,0] = recvbuf[:]


def evolve_np_slicing(grid, grid_tmp):
    """Time step based on an explicitly coded Laplacian using array slicing."""
    # only change here: parallel BCs
    #apply_periodic_boundary_conditions(grid)
    apply_periodic_boundary_conditions_mpi(grid)
    grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + dt * D * (
        grid[0:-2, 1:-1] + grid[2:, 1:-1] + grid[1:-1, 0:-2] + grid[1:-1, 2:]
        - 4.0 * grid[1:-1, 1:-1])


# call time evolution as in serial case
grid_ini = init()
grid = init()
grid_tmp = np.empty_like(grid)
main_loop(evolve_np_slicing, grid, grid_tmp)

# plot local data for each rank
import matplotlib.pyplot as plt
f = plt.figure(figsize=(10,5))
plt.subplot(121)
plt.pcolormesh(grid_ini.T)
plt.axis('image')
plt.title(f'Initial (rank {rank})')
plt.subplot(122)
plt.pcolormesh(grid.T)
plt.axis('image')
plt.title(f'Evolved (rank {rank})')
f.savefig(f'diffusion{rank}.png', dpi=300)

# Get global array on rank 0 to plot it
grid_global = np.empty((n_global, n_global))
if rank == 0:
    # set data from rank 0
    grid_global[edges_x[index_x]:edges_x[index_x+1],
                edges_y[index_y]:edges_y[index_y+1]] = grid[1:-1, 1:-1]
    # now get data from all other ranks
    for src in range(1, n_proc):
        # determine size of data to be received
        i_x, i_y = cart.Get_coords(src)
        # allocate array
        grid_rcv = np.empty([sizes_x[i_x], sizes_y[i_y]])
        comm.Recv(grid_rcv, source=src)
        # set corresponding part of global array
        grid_global[edges_x[i_x]:edges_x[i_x+1],
                    edges_y[i_y]:edges_y[i_y+1]] = grid_rcv[:, :]
else:
    # send grid without halo points to root process
    # need to copy, non-contiguous arrays not allowed
    grid_send = grid[1:-1, 1:-1].copy()
    comm.Send(grid_send, 0)

# plot global grid from rank 0
if rank == 0:
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(5,5))
    plt.subplot(111)
    plt.pcolormesh(grid_global.T)
    plt.axis('image')
    plt.title('Global grid at end')
    f.savefig('diffusion_global.png', dpi=300)


# write output
# set this to true if you have an h5py version supporting parallel hdf5
write_output_parallel = False

if write_output_parallel = True
    # Output data in parallel with hdf5
    f = h5py.File('parallel.hdf5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
    # create dataset of global size
    dset = f.create_dataset('test', (n_global, n_global), dtype='d')
    # set local data
    dset[edges_x[index_x]:edges_x[index_x+1],
         edges_y[index_y]:edges_y[index_y+1]] = grid[1:-1, 1:-1]
    f.close()
else:
    # write only from rank 0
    if rank == 0:
        f = h5py.File('serial.hdf5', 'w')
        # create dataset of global size
        dset = f.create_dataset('test', (n_global, n_global), dtype='d')
        # set global data array
        dset[:, :] = grid_global[:, :]
        f.close()
