FC ?= gfortran
MPIFC ?= mpif90

all: diff.exe

diff.exe: diff.F90
	$(FC) -O3 -march=native -fopt-info-vec -fopenmp -o $@ $<

diff_mpi.exe: diff_mpi.F90
	$(MPIFC) -O3 -march=native -fopt-info-vec -fopenmp -o $@ $<

.PHONY: clean
clean:
	rm -f diff_mpi.exe diff.exe *.o *.mod

