from setuptools import setup
setup(
    name="HelloWorld",
    version="0.1",
    # specify a list of the packages (subdirectory with __init__.py file)
    packages=["HelloWorld"],
    # executable that comes with the package (if applicable)
    scripts=['say_hello.py'],
    # software dependencies (if necessary)
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    # metadata for upload to PyPI
    author="Me",
    author_email="me@example.com",
    description="This is an Example Package",
    license="PSF",
    keywords="hello world example examples",
    url="http://example.com/HelloWorld/",   # project home page, if any
)
