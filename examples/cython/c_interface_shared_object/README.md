# Example Python package "wrap_libhello", illustrating a simple Cython-C binding of a shared object (i.e. existing C library)

## Features

* Python module "hello" lives in the package-directory "wrap_libhello" (has `__init__.py`)
* `hello.pyx` contains the Python interface written in Cython
* `c_hello.c` contains a hello-world implementation in C, however, in contrast
  to the previous simple example it is located in a different library (.so,
  shared object) in the directory `libhello`.
  Use `make` to generate the shared object in that directory.
* `setup.py` contains code to compile the extension, demonstrating how to link
  the shared object in a stable way.

## Usage

* set enviroment variable HELLO_ROOT to point to libhello, e.g., from
  the current directory `export HELLO_ROOT=$(pwd)/libhello/`
* quick test in the current directory
  `pip install -e --user .`
  run `test_wrap_libhello.py` to call the function in the shared object
* or install the package, and run the extension from anywhere
  `python install . --user`
