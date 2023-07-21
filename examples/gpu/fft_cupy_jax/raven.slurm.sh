#!/bin/bash
#SBATCH -o ./job.out.%j
#SBATCH -D ./
#SBATCH -J PythonGPU
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=18
#SBATCH --gres=gpu:a100:1
#SBATCH --time=00:05:00
#SBATCH --partition=gpudev
module purge
module load anaconda/3/2023.03 cuda/12.1 cupy/12.1 cudnn/8.9.0 jax/0.4.13
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
srun nvidia-smi -L | grep 'GPU 0'
srun python3 fft_scipy_cupy_jax.py
