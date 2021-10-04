#!/bin/bash -l
#
# Example job script for using MPI4PY on Cobra@MPCDF.
#
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MPI
#SBATCH --mail-type=none
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00   # run time in h:m:s, up to 24h possible

module purge
module load gcc/10 impi/2019.9
module load anaconda/3/2021.05
module load mpi4py/3.0.3

# avoid overbooking of the cores which would occur via NumPy/MKL threading
# as the parallelization takes place via MPI tasks
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

srun python ./python_mpi4py.py
