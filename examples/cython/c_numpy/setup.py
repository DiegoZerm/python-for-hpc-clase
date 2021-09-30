import os
import numpy as np
from setuptools import setup, Extension


# assuming gcc, set (aggressive) optimization flags, to be appended to the default compile line
c_flags = []
c_flags.append("-O3")
c_flags.append("-ffast-math")
c_flags.append("-fopenmp")
c_flags.append("-march=native")
c_flags.append("-fPIC")
c_flags.append("-fopt-info")

# include directories
include_dirs = []
include_dirs.append(np.get_include())

# extra link flags are possible as well; we leave them empty here
ld_flags = []

ext = Extension("ctonumpy.cube",
                sources=["ctonumpy/cube.pyx", "ctonumpy/c_cube.c"],
                extra_compile_args=c_flags,
                extra_link_args=ld_flags,
                include_dirs=[np.get_include()])

setup(name="ctonumpy",
      ext_modules=[ext],
)

