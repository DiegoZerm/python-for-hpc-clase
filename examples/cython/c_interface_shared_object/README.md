# Example Python package "wrap_libhello", illustrating a simple Cython-C binding of a shared object (i.e. existing C library)

## Features

* Python module "wrap_libhello" lives in the directory "wrap_libhello" (has `__index__.py`)
* `hello.pyx` contains the Python interface written in Cython
* `c_hello.c` contains a hello-world implementation in C, however, in contrast
  to the previous simple example it is located in a different library (.so,
  shared object) in the directory `libhello`.  Use `make` to generate the
  shared object.
* `setup.py` contains code to compile the extension, demonstrating how to link
  the shared object in a stable way

## Usage

* quick test in the current directory
  `python setup.py build_ext --inplace`
  `python -c "from wrap_libhello import hello; hello.say_hello()"`
* or install the package, and run the extension from anywhere
  `python setup.py install --user`
* run `test_wrap_libhello.py` to call the function in the shared object
