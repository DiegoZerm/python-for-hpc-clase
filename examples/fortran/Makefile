all: diff.exe

diff.exe: diff.F90
	gfortran -O3 -march=native -fopt-info-vec -fopenmp -fno-strict-aliasing -o $@ $<

diff_mpi.exe: diff_mpi.F90
	mpif90 -O3 -march=native -fopt-info-vec -fopenmp -fno-strict-aliasing -o $@ $<

.PHONY: clean
clean:
	rm -f diff_mpi.exe diff.exe *.o *.mod

