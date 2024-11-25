# Cython interface to the <c_cube.{c,h}> code.
# For more detailed explanations please confer
# http://cython.readthedocs.io/en/latest/src/tutorial/numpy.html

import numpy as np
cimport numpy as np

cdef extern from "c_cube.h":
    void cube(double*, double*, int)

def compute(np.ndarray v):
    """Cube each element of the NumPy array v, and return a new NumPy array
    with the same dimensions containing the result values.
    """
    assert(v.dtype == np.float64)
    # Note: The following line allocates the memory, the deallocation is done
    # later in the Python layer when the object goes out of scope.
    cdef np.ndarray w = np.empty_like(v)
    cdef int n = v.size
    cube(<double*>v.data, <double*>w.data, n)
    return w

