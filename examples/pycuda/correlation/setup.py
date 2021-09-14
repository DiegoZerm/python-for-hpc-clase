from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import os

incl_dirs = [np.get_include()]

ext_modules=[
    Extension("corr",
              sources=["corr.pyx"],
              include_dirs=incl_dirs,
              libraries=["m"] # Unix-like specific
    )
]


setup(
  name = 'Correlation',
  description = 'compute velocity correlations',
  author = 'Sebastian Ohlmann',
  version = '1.0',
  #ext_modules = cythonize("corr.pyx"),
  ext_modules = cythonize(ext_modules),
)
