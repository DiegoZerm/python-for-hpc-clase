#!/bin/bash

# NOTE: requires `pip install --user line_profiler`

kernprof -l ./diffusion_naive.py

python -m line_profiler diffusion_naive.py.lprof
