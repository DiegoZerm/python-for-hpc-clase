#!/usr/bin/env python

import fib

print("# automatically generated docstring")
print(fib.fib.__doc__)

a = fib.fib(16)

print("# return object is a NumPy array")
print(type(a))

print("# Fibonacci numbers")
print(a)

