# Python for HPC

Welcome to the MPCDF **Python for HPC** course!

## Authors

* 2022 - 2024 Sebastian Kehl (sebastian.kehl@mpcdf.mpg.de)
* 2020        Rafael Lago
* 2018 - 2024 Sebastian Ohlmann (sebastian.ohlmann@mpcdf.mpg.de)
* 2018 - 2024 Klaus Reuter (klaus.reuter@mpcdf.mpg.de)

[Max Planck Computing and Data Facility, Garching](https://mpcdf.mpg.de/)

## Course material

* This material is currently intended to be used only by the registered participants of a Python for HPC course given by the MPCDF
* Redistribution requires the consent of the authors
* A git repository of the material is provided at https://gitlab.mpcdf.mpg.de/mpcdf/python-for-hpc-exercises
* The Jupyter notebooks discussed during the lectures are bundled into a [Jupyter book](https://mpcdf.pages.mpcdf.de/python-for-hpc) for convenient reading.

## List of topics

* Introduction
  * Python refresher
  * Basic HPC
* Efficient numerical computing
  * NumPy
  * SciPy
  * HDF5-based IO with h5py
  * Cython
  * Interfacing with C/C++, Fortran, CUDA, and libraries
  * JIT, Numba, Jax
  * Profiling
* Parallel computing
  * Parallel computing basics
  * Python threading, GIL
  * multiprocessing
  * GPU computing using Numba, CuPy, Jax
  * Parallelization frameworks, e.g. Dask
  * mpi4py
  * Running parallel Python programs with Slurm
* Software engineering with Python
  * Testing
  * Packaging
  * Documentation
* Visualization
  * matplotlib
  * Colors
* Exercises and examples
  * Basic Python
  * NumPy
  * simple advection code
  * simple diffusion code (MPI)

## References

This course is largely based on our experience from daily work. In addition, the following sources were used:

* *High Performance Python, Practical Performant Programming for Humans*, Micha Gorelick, Ian Ozsvald, O'Reilly Media; Second Edition, 2020. (In particular, parts of the diffusion example are discussed similarly to the presentation in this book.)
* *A Whirlwind Tour of Python*, Jake VanderPlas, O'Reilly Media, 2016. 
* official documentation of Python, NumPy, SciPy, Cython, Numba, mpi4py, etc.

Other (minor) sources are referenced directly in the notebooks.

## Software prerequisites

### Python packages

The examples discussed in this course are based on Python 3 and NumPy, SciPy,
Cython, Numba, matplotlib, mpi4py, Dask, and few more.

To conveniently get access to all the required packages, users can download and install
[Miniforge](https://conda-forge.org/miniforge/) -- which is a free alternative to
commercial Python distributions -- and use `conda` or `mamba` together with the file
`environment.yml` from this repository to create a local
[software environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

### Jupyter presentation via RISE

* Presentation of the Jupyter notebook cells as slides is possible via the [RISE](http://rise.readthedocs.io/en/latest/index.html) extension.
  * To enter presentation mode, simply press <Alt+r> from within a notebook.

