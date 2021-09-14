#!/bin/bash -l

#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MPI
#SBATCH --mail-type=none
###SBATCH --partition=general   # note: general partition is necessary on DRACO for jobs with >1 nodes, not on COBRA
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --time=00:01:00   # run time in h:m:s, up to 24h possible

module purge
module load gcc/10 impi/2019.8
module load anaconda/3/2019.03
module load mpi4py

# avoid overbooking of the cores which might occur via NumPy/MKL threading
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

srun python ./python_mpi4py.py
