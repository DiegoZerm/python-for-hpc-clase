#!/bin/bash -l
#
# Example job script for using Python with Multithreading (OpenMP, Numba, numexpr) on Cobra@MPCDF.
#
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MT
#SBATCH --mail-type=none
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1   # only start 1 task via srun because Python multiprocessing starts more tasks internally
#SBATCH --cpus-per-task=40    # assign all the cores to that first task to make room for Python's multiprocessing tasks
#SBATCH --time=00:10:00

module purge
module load gcc/10 impi/2019.9
module load anaconda/3/2021.05

# set the correct number of threads for various thread-parallel modules
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMBA_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_NUM_THREADS=$SLURM_CPUS_PER_TASK
# pin OpenMP threads to cores
export OMP_PLACES=cores

srun python ./python_multithreading.py
