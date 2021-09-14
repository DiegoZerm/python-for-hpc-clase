#!/bin/bash -l

#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MP
#SBATCH --mail-type=none
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1   # only start 1 task via srun because Python multiprocessing starts more tasks internally
#SBATCH --cpus-per-task=32    # assign all the cores to that first task to make room for Python's multiprocessing tasks
#SBATCH --time=00:01:00

module purge
module load gcc/10 impi/2019.8
module load anaconda/3/2019.03

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun python ./python_multithreading.py
