from setuptools import setup

setup(
    # name of the software package (as it would appear on PyPI)
    name="helloworld",
    version="0.1",
    # list of the Python modules provided by the package
    packages=["helloworld"],
    # list of executable(s) that come with the package (if applicable)
    scripts=['say_hello.py'],
    # list of package dependencies (if necessary)
    #install_requires=['numpy'],
    # more information, necessary for an upload to PyPI
    author="John Doe",
    author_email="john.doe@example.mpg.de",
    description="example package that prints hello world",
    license="PSF",
    keywords="hello world example",
    url="https://example.mpg.de/helloworld/",   # project home page, if any
)
