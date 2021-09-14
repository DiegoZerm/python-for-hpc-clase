#!/bin/bash

python -m cProfile -s cumtime \
    ./diffusion_naive.py \
        &>cprofile.log
