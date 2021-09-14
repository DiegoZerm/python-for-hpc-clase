#!/bin/bash

# * requires perf on a Linux system
# * to run as a regular user, issue as root
#   echo 0 >/proc/sys/kernel/perf_event_paranoid

#EVENTS=""
EVENTS="-e fp_arith_inst_retired.128b_packed_double -e fp_arith_inst_retired.256b_packed_double -e fp_arith_inst_retired.scalar_double"


# no fp vectorization
perf stat -d $EVENTS ./diffusion_naive.py

# AVX2 vectorization
perf stat -d $EVENTS ./diffusion_numba.py

