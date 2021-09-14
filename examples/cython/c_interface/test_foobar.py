#!/usr/bin/env python

try:
    from foobar import hello
except:
    print("Please compile first using `python setup.py build_ext --inplace`")
else:
    hello.say_hello()

