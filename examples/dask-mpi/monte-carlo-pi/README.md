# Distributed Monte-Carlo pi computation based on Dask, optionally Dask_MPI

## Purpose

'dask-mc-pi.py' implements the simple Monte-Carlo algorithm to determine pi.
Individual tasks are submitted via 'delayed()' followed by a final averaging task.
The MPI backend of Dask can be enabled to test the program on a HPC cluster.

## Usage

The program can be either launched via MPI or conventionally.
Make sure to adapt the parameters in the program to enable/disable MPI.
A Slurm jobscript for MPCDF Raven is provided to run with Dask_MPI.