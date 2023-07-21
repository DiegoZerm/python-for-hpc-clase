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
module load anaconda/3/2023.03 cuda/11.6
srun python3 numba_gpu.py
