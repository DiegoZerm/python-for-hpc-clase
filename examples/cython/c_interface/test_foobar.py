#!/usr/bin/env python

try:
    from foobar import hello
except:
    print("Please compile first using `pip install -e .`")
else:
    hello.say_hello()

