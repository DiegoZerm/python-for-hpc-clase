#!/bin/bash

f2py -c fib.f90 -m fib --opt="-O3 -march=native" --verbose

