# implementation file, part of the "HelloWorld" demo Python package

def say_hello():
    print("Hello World!")

def eigen(matrix):
    import numpy.linalg as LA
    return LA.eig(matrix)
