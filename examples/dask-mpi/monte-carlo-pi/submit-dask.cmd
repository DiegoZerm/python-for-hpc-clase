#!/bin/bash -l
#SBATCH -D ./
#SBATCH -o job.%x.out.%j
#SBATCH -e job.%x.err.%j
#SBATCH -J dask-mc-pi
#SBATCH --ntasks=8
#SBATCH --mem=24000
#SBATCH --time=00:05:00

# MPCDF Raven, 2022/11

module purge
module load anaconda/3/2021.11 gcc/11 impi/2021.6 mpi4py/3.0.3
# based on these modules, we require in addition the following user-local installation (i.e. run the following command once)
# `pip install dask_mpi jupyter-server-proxy graphviz --user`

srun python3 dask-mc-pi.py

