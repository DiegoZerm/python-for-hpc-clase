// pybind11 example module 'pybex'

#include <vector>
#include <numeric>
#include <functional>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


// C/C++ implementation of the function to be wrapped
void c_cube(const double * v_in, double * v_out, size_t n_elem) {
    #pragma omp parallel for simd default(none) shared(v_in, v_out, n_elem)
    for (size_t i=0; i<n_elem; ++i) {
        v_out[i] = v_in[i] * v_in[i] * v_in[i];
    }
}


namespace py = pybind11;

// wrapper function, accepting a NumPy array as input and returning a NumPy array
py::array_t<double> py_cube(py::array_t<double, py::array::c_style> np_in)
{
    // obtain information about the input array
    py::buffer_info pybuf_in = np_in.request();
    auto shape = pybuf_in.shape;

    // create output NumPy array of the same size and dimension
    py::array_t<double, py::array::c_style> np_out(shape);

    // call C/C++ function with proper arguments
    double * pybuf_in_ptr = (double*) pybuf_in.ptr;
    double * pybuf_out_ptr = (double*) np_out.request().ptr;
    size_t count = std::accumulate(shape.begin(), shape.end(), 1, std::multiplies<size_t>());
    c_cube(pybuf_in_ptr, pybuf_out_ptr, count);

    return np_out;
}


// define Python module, expose py_cube function as "cube" to python
PYBIND11_MODULE(pybex, m) {
    m.doc() = "pybind11 example module"; // module docstring

    m.def("cube", &py_cube, "a function that cubes a double-precision numpy array");
}

