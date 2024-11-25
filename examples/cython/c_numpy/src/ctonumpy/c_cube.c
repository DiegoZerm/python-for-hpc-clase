#include "c_cube.h"

void cube(double * v_in, double * v_out, int n_elem) {
    #pragma omp parallel for simd default(none) shared(v_in, v_out, n_elem)
    for (int i=0; i<n_elem; ++i) {
        v_out[i] = v_in[i] * v_in[i] * v_in[i];
    }
}
