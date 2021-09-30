from setuptools import setup
# run `pip install --user pybind11` if not yet installed
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "pybex",
        ["src/pybex.cpp",],
    ),
]

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules
)

