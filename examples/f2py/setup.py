#!/usr/bin/env python

from numpy.distutils.core import setup, Extension

ext = Extension(name = 'fib',
                sources = ['fib.f90'])

setup(name = 'f2py_example',
      ext_modules = [ext])
