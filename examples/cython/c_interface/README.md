# Example Python package "foobar", illustrating a simple Cython-C binding

## Features

* Python module "foobar.hello" lives in the directory "foobar" (has `__index__.py`)
* `c_hello.c` contains a hello-world implementation in C
* `hello.pyx` provides the module 'foobar.hello' and contains the Python interface written in Cython
* `setup.py` contains code to compile the extension, both the source files are compiled into the same shared object

## Usage

* quick test in the current directory
  `python setup.py build_ext --inplace`
  `python -c "from foobar import hello; hello.say_hello()"`
* or install the package, and run the extension from anywhere
  `python setup.py install --user`
* run `test_foobar.py` to call the compiled code example

