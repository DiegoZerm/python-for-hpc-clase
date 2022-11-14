from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

# extra compile/link args may be injected, e.g. here for optimization and openmp with gcc
extra_gcc_args=['-O3', '-march=native', '-fopenmp']

ext_modules = [
    Pybind11Extension(
        "pybex",
        ["src/pybex.cpp",],
        extra_compile_args=extra_gcc_args,
        extra_link_args=extra_gcc_args
    ),
]

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules
)

