#!/bin/bash -l
#SBATCH -D ./
#SBATCH -o job.%x.out.%j
#SBATCH -J dask-mc-pi
#SBATCH --ntasks=8
#SBATCH --mem=24000
#SBATCH --time=00:04:00

# MPCDF Raven, 2023/07
module purge
module load gcc/13 anaconda/3/2023.03 impi/2021.9 mpi4py/3.1.4 dask-mpi/2022.4

export OMP_NUM_THREADS=1

srun python3 dask-mc-pi.py

