# Example Python package "ctonumpy", illustrating a Cython-C binding that accesses NumPy arrays

## Features

* Python module "ctonumpy" lives in the directory "ctonumpy" (has `__init__.py`)
* `c_cube.c` contains a OMP parallel loop-based computation of the third power of an array
* `cube.pyx` contains the Python interface written in Cython
* `setup.py` contains code to compile the extension with optimizing compiler flags
* `test_ctonumpy.py` is a driver routine to run the extension and check against a NumPy result

## Usage

* quick test in the current directory  
  `python setup.py build_ext --inplace`  
  `./test_ctonumpy.py`
* or install the package, and run the extension from anywhere

