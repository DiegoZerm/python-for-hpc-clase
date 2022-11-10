# Minimal Cython example, demonstrating the compilation using <setup.py>

Run the following commands to build and run the example:
1.  python setup.py config
2.  pip install -e .
3.  python -c "import hello_world; hello_world.say_hello()"

Explanation:
1.  check prerequisites, translate the .pyx code into .c code using `cython`
2.  run the system compiler (typ. `gcc`) on the .c code, create .so Python module
3.  run the example
