#!/bin/bash -l

#SBATCH -J PYTHON          # job name
#SBATCH -o ./job.out.%j    # standard out file
#SBATCH -e ./job.err.%j    # standard err file
#SBATCH -D ./              # work directory
#SBATCH --ntasks=1         # launch job on a single core
#SBATCH --cpus-per-task=1  #   on a shared node
#SBATCH --mem=2000MB       # memory limit for the job
#SBATCH --time=0:29:59     # run time, up to 24h
# Important: You must use the small partition on DRACO for jobs on a shared node,
# so enable the following line when running on DRACO:
###SBATCH --partition=small

module purge
module load gcc/10 impi/2019.8
module load anaconda/3/2019.03

# avoid overbooking of the cores which might occur via NumPy/MKL threading
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

srun python ./python_hello_world.py
