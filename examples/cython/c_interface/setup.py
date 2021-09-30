import os
from setuptools import setup, Extension

ext = Extension("foobar.hello",
                sources=["foobar/hello.pyx", "foobar/c_hello.c"])

setup(name="foobar",
      ext_modules=[ext],
)
