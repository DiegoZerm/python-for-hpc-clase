import os
from setuptools import setup, Extension, Command

ext = Extension("foobar.hello",
                sources=["foobar/hello.pyx", "foobar/c_hello.c"])

class CleanCommand(Command):
    """Enable `python setup.py clean` to tidy up properly."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf build')
        os.system('rm -vrf dist')
        os.system('rm -vrf foobar/hello.c')
        os.system('rm -vrf foobar/__pycache__')
        os.system('rm -vrf foobar.egg-info')
        os.system("find foobar -name '*.so' -delete -print")
        os.system("find foobar -name '*.pyc' -delete -print")


setup(name="foobar",
      ext_modules=[ext],
      cmdclass={'clean': CleanCommand})
