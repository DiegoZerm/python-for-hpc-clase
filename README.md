# Python for HPC

Welcome to the MPCDF **Python for HPC** tutorial!

## Authors

* © 2018 - 2021 Sebastian Ohlmann (sebastian.ohlmann@mpcdf.mpg.de)
* © 2018 - 2021 Klaus Reuter (klaus.reuter@mpcdf.mpg.de)
* © 2020 Rafael Lago (rafael.lago@mpcdf.mpg.de)

[Max Planck Computing and Data Facility, Garching](https://mpcdf.mpg.de/)

## Course material

A tarball containing the course material is available for
[download](https://mpcdf.pages.mpcdf.de/python-for-hpc/pyhpc.tar.gz).

The Jupyter notebooks discussed during the lectures are bundled into a
[Jupyter book](https://mpcdf.pages.mpcdf.de/python-for-hpc) for convenient reading.

* This material is currently intended to be used only by the registered participants of a Python for HPC course given by the MPCDF
* Redistribution requires the consent of the authors

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
  * Numba
  * Profiling
* Parallel computing
  * Parallel computing basics
  * Python threading, GIL
  * multiprocessing
  * mpi4py
  * Running parallel Python programs with SLURM
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
* official documentation of Python, NumPy, SciPy, Cython, Numba, mpi4py

Other minor sources are referenced in the notebooks.

## Software prerequisites

### Installation of the Anaconda Python Distribution

The examples discussed in this course are based on Python 3 and NumPy, SciPy,
Cython, Numba, etc.
To conveniently get access to all those packages, you can download and install
Anaconda Python 3 into your home directory by using the script
`aux/install_anaconda.sh`

### Jupyter presentation via RISE

* Presentation of the Jupyter notebook cells as slides is possible via the [RISE](http://rise.readthedocs.io/en/latest/index.html) extension.
  * Installation
    * `pip install RISE`
    * `jupyter-nbextension install rise --py --sys-prefix`
    * `jupyter-nbextension enable rise --py --sys-prefix`
  * To enter presentation mode, simply press <Alt+r> from within a notebook.
