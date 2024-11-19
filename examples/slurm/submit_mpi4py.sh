#!/bin/bash -l
#
# Example job script for using MPI4PY on Raven@MPCDF.
#
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MPI
#SBATCH --mail-type=none
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=72
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00   # run time in h:m:s, up to 24h possible

module purge
module load gcc/13 openmpi/4.1
module load anaconda/3/2023.03
module load mpi4py/3.1.5

# avoid overbooking of the cores which would occur via NumPy/MKL threading
# as the parallelization takes place via MPI tasks
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

srun python3 ./python_mpi4py.py
