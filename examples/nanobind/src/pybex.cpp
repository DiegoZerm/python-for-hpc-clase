// nanobind example module 'pybex'

#include <vector>
#include <numeric>
#include <functional>

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

namespace nb = nanobind;

// C/C++ implementation of the function to be wrapped
void c_cube(const double * v_in, double * v_out, size_t n_elem) {
    #pragma omp parallel for simd default(none) shared(v_in, v_out, n_elem)
    for (size_t i=0; i<n_elem; ++i) {
        v_out[i] = v_in[i] * v_in[i] * v_in[i];
    }
}

using array = nb::ndarray<double, nb::numpy, nb::c_contig>;

// wrapper function, accepting a NumPy array as input and returning a NumPy array
array py_cube(array np_in)
{
    // create output buffer
    double *out_buffer = new double[np_in.size()];

    // call C/C++ function with proper arguments
    c_cube(np_in.data(), out_buffer, np_in.size());

    // Delete 'data' when the 'owner' capsule expires
    nb::capsule owner(out_buffer, [](void *p) noexcept {
       delete[] (double *) p;
    });

    return array(out_buffer, np_in.ndim(), (const size_t*)np_in.shape_ptr(), owner);
}


// define Python module, expose py_cube function as "cube" to python
NB_MODULE(_pybex, m) {
    m.doc() = "nanobind example module"; // module docstring

    m.def("cube", &py_cube, "a function that cubes a double-precision numpy array");
}

