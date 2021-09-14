cdef extern from "c_hello.h":
    void hello()

def say_hello():
    hello()
