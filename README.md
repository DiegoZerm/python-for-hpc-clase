# Python for HPC

Welcome to the MPCDF **Python for HPC** course!

## Authors

* 2022 - 2023 Sebastian Kehl (sebastian.kehl@mpcdf.mpg.de)
* 2020        Rafael Lago
* 2018 - 2023 Sebastian Ohlmann (sebastian.ohlmann@mpcdf.mpg.de)
* 2018 - 2023 Klaus Reuter (klaus.reuter@mpcdf.mpg.de)

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

* *High Performance Python, Practical Performant Programming for Humans*, Micha Gorelick, Ian Ozsvald, O'Reilly Media; 2014. (In particular, parts of the diffusion example are discussed similarly to the presentation in this book.)
* *A Whirlwind Tour of Python*, Jake VanderPlas, O'Reilly Media, 2016. 
* official documentation of Python, NumPy, SciPy, Cython, Numba, mpi4py, etc.

Other minor sources are referenced in the notebooks.

## Software prerequisites

### Python packages

The examples discussed in this course are based on Python 3 and NumPy, SciPy,
Cython, Numba, matplotlib, and few more.
To conveniently get access to all those packages, you can e.g. download and install
Anaconda Python or a similar distribution and add additional required packages
using `pip` or `conda`. The 'environment.yml' file can be used for `conda`.

### Jupyter presentation via RISE

* Presentation of the Jupyter notebook cells as slides is possible via the [RISE](http://rise.readthedocs.io/en/latest/index.html) extension.
  * Installation
    * `pip install RISE`
    * `jupyter-nbextension install rise --py --sys-prefix`
    * `jupyter-nbextension enable rise --py --sys-prefix`
  * To enter presentation mode, simply press <Alt+r> from within a notebook.

