import os
from setuptools import setup, Extension

try:
    libhello_root = os.environ["HELLO_ROOT"]
except KeyError as e:
    raise ValueError("Set path to libhello in environment variable HELLO_ROOT")

libhello_dir = os.path.abspath(libhello_root)

# We need to specify the location of the include file.
include_dirs = []
include_dirs.append(libhello_dir)

# Extra link flags are necessary to link the shared object, in addition
# we add an RPATH to enable our Python module to locate the library at run time
# without the need to set LD_LIBRARY_PATH.
ld_flags = []
ld_flags.append("-L"+libhello_dir)
ld_flags.append("-Wl,-rpath,"+libhello_dir)
ld_flags.append("-lhello")  # link libhello

ext = Extension("wrap_libhello.hello",
                sources=["wrap_libhello/hello.pyx"],
                extra_link_args=ld_flags,
                include_dirs=include_dirs
)

setup(
    ext_modules=[ext],
)
