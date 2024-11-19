#!/bin/bash -l
#
# Example job script for using Python-Multiprocessing on Raven@MPCDF.
#
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MP
#SBATCH --mail-type=none
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1   # only start 1 task via srun because Python multiprocessing starts more tasks internally
#SBATCH --cpus-per-task=72    # assign all the cores to that first task to make room for Python's multiprocessing tasks
#SBATCH --time=00:10:00

module purge
module load gcc/13 openmpi/4.1
module load anaconda/3/2023.03

# avoid overbooking of the cores which might occur via NumPy/MKL threading,
# as the parallelization takes place via processes/multiprocessing
export OMP_NUM_THREADS=1

# pass the number of available cores via the command line, and
# use that number to spawn as many workers from multiprocessing
srun python3 ./python_multiprocessing.py $SLURM_CPUS_PER_TASK
