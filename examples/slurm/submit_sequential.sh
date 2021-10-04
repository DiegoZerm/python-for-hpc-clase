#!/bin/bash -l
#
# Example Slurm job script for a small sequential Python program on MPCDF systems.
#
#SBATCH -J PYTHON          # job name
#SBATCH -o ./job.out.%j    # standard out file
#SBATCH -e ./job.err.%j    # standard err file
#SBATCH -D ./              # work directory
#SBATCH --ntasks=1         # launch job on a single core
#SBATCH --cpus-per-task=1  #   on a shared node
#SBATCH --mem=2000MB       # memory limit for the job
#SBATCH --time=0:10:00     # run time, up to 24h

module purge
module load gcc/10 impi/2019.9
module load anaconda/3/2021.05

# avoid overbooking of the cores which might occur via NumPy/MKL threading
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

srun python ./python_hello_world.py
