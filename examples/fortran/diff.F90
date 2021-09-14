module diff2d_mod
    implicit none
contains
    subroutine initial_condition(grid, np)
        integer, intent(in) :: np
        double precision, intent(inout) :: grid(0:np+1, 0:np+1)
        integer :: block_lo, block_hi
        block_lo = int(0.4 * real(np))
        block_hi = int(0.6 * real(np))
        grid(block_lo:block_hi, block_lo:block_hi) = 0.005
    end subroutine

    subroutine apply_periodic_boundary_conditions(grid, np)
        integer, intent(in) :: np
        double precision, intent(inout) :: grid(0:np+1, 0:np+1)
        grid(  0,   :) = grid(np, :)
        grid(np+1,   :) = grid(1, :)
        grid(  :,   0) = grid(:, np)
        grid(  :, np+1) = grid(:, 1)
    end subroutine

    subroutine evolve(grid, grid_new, np, dt, D)
        integer, intent(in) :: np
        double precision, intent(in) :: grid(0:np+1, 0:np+1)
        double precision, intent(out) :: grid_new(0:np+1, 0:np+1)
        double precision, intent(in) :: dt, D
        integer ix, iy
!$omp parallel do default(shared) private(ix,iy)
        do ix=1,np
            do iy=1,np
                grid_new(iy,ix) = grid(iy,ix) + dt * D * &
                                  (  grid(iy-1,ix) + grid(iy+1,ix) &
                                   + grid(iy,ix-1) + grid(iy,ix+1) &
                                   - 4. * grid(iy,ix))
            enddo
        enddo
!$omp end parallel do
    end subroutine evolve
end module diff2d_mod

program diff2d
    use omp_lib
    use diff2d_mod
    implicit none

    double precision, allocatable, target :: grid_1(:,:), grid_2(:,:)
    double precision, pointer :: grid(:,:), grid_new(:,:), grid_tmp(:,:)
    integer :: fp, i, n_iterations, np
    double precision :: dt, D, t0
    namelist /diff/ n_iterations, np, dt, D

    open(newunit=fp, file="diff_par.nml", status='old', action='read')
    read(fp, diff)
    close(fp)

    allocate(grid_1(0:np+1, 0:np+1))
    allocate(grid_2(0:np+1, 0:np+1))

    grid => grid_1
    grid_new => grid_2

    call initial_condition(grid_1, np)

    t0 = omp_get_wtime()

    do i=1,n_iterations
        call apply_periodic_boundary_conditions(grid, np)
        call evolve(grid, grid_new, np, dt, D)
        grid_tmp => grid_new
        grid_new => grid
        grid => grid_tmp
        if (modulo(i,100) == 0) &
            write(*,*) int(100.0 * real(i)/real(n_iterations)), "%"
    enddo

    write(*,*) "main loop time =", omp_get_wtime() - t0

    deallocate(grid_1)
    deallocate(grid_2)
end program diff2d
