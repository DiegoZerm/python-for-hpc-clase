// pybind11 example module 'pybex'

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// C/C++ implementation of the function to be wrapped
void c_cube(const double * v_in, double * v_out, size_t n_elem) {
    for (size_t i=0; i<n_elem; ++i) {
        v_out[i] = v_in[i] * v_in[i] * v_in[i];
    }
}

// wrapper function, accepting a NumPy array as input and returning a NumPy array
py::array_t<double> py_cube(py::array_t<double, py::array::c_style> v_in)
{
  // allocate buffer to be returned as a NumPy array
  auto v_out = py::array_t<double>(v_in.size());
  double * v_out_ptr = (double*) v_out.request().ptr;

  c_cube(v_in.data(), v_out_ptr, v_in.size());

  return v_out;
}

PYBIND11_MODULE(pybex, m) {
    m.doc() = "pybind11 example module"; // module docstring

    m.def("cube", &py_cube, "a function that cubes a double-precision numpy array");
}

