module diff2d_mod
    use mpi
    implicit none
    integer, parameter :: nd = 2
    integer, parameter :: up = 1
    integer, parameter :: down = 2
    integer, parameter :: left = 3
    integer, parameter :: right = 4
    type mpi_stuff
        integer :: world_size
        integer :: world_rank
        integer :: cart_comm
        integer :: cart_rank
        integer :: cart_coords(nd)
        integer :: cart_neighbors(2*nd)
    end type mpi_stuff
contains
    subroutine mpi_setup(mp)
        type(mpi_stuff), intent(inout) :: mp
        integer :: dims(nd), per_dim
        logical :: periods(nd), reorder
        integer :: ierr
        call mpi_init(ierr)
        call mpi_comm_size(MPI_COMM_WORLD, mp%world_size, ierr)
        call mpi_comm_rank(MPI_COMM_WORLD, mp%world_rank, ierr)
        per_dim = nint(sqrt(real(mp%world_size)))
        if ((per_dim*per_dim) /= mp%world_size) then
            if (mp%world_rank == 0) &
                write(*,*) "Error: The number of processors must be a square number."
            call mpi_finalize(ierr)
            stop
        else
            dims(:) = per_dim
            periods(:) = .true.
            reorder = .true.
            call mpi_cart_create(MPI_COMM_WORLD, nd, dims, periods, reorder, mp%cart_comm, ierr)
            call mpi_comm_rank(mp%cart_comm, mp%cart_rank, ierr)
            call mpi_cart_coords(mp%cart_comm, mp%cart_rank, nd, mp%cart_coords, ierr)
            call mpi_cart_shift(mp%cart_comm, 0, 1, mp%cart_neighbors(down), mp%cart_neighbors(up), ierr)
            call mpi_cart_shift(mp%cart_comm, 1, 1, mp%cart_neighbors(left), mp%cart_neighbors(right), ierr)
            ! write(*,*) "MPI setup : ", mp%cart_rank, mp%cart_coords, mp%cart_neighbors
        endif
    end subroutine mpi_setup

    subroutine mpi_teardown(mp)
        type(mpi_stuff), intent(inout) :: mp
        integer :: ierr
        call mpi_finalize(ierr)
    end subroutine mpi_teardown

    subroutine initial_condition(grid, np)
        integer, intent(in) :: np
        double precision, intent(inout) :: grid(0:np+1, 0:np+1)
        integer :: block_lo, block_hi
        block_lo = int(0.01 * real(np))
        block_hi = int(0.4 * real(np))
        grid(block_lo:block_hi, block_lo:block_hi) = 0.005
        block_lo = int(0.6 * real(np))
        block_hi = int(0.99 * real(np))
        grid(block_lo:block_hi, block_lo:block_hi) = 0.005
    end subroutine

    subroutine apply_periodic_boundary_conditions(grid, mp, np)
        integer, intent(in) :: np
        type(mpi_stuff), intent(inout) :: mp
        double precision, intent(inout) :: grid(0:np+1, 0:np+1)
        double precision, allocatable :: buf_tx(:), buf_rx(:)
        integer, parameter :: mpi_tag = 0
        integer :: ierr
        allocate(buf_tx(np))
        allocate(buf_rx(np))
        ! up
        buf_tx(:) = grid(np, 1:np)
        call mpi_sendrecv(buf_tx, np, mpi_double_precision, mp%cart_neighbors(up), mpi_tag, &
                          buf_rx, np, mpi_double_precision, mp%cart_neighbors(down), mpi_tag, &
                          mp%cart_comm, MPI_STATUS_IGNORE, ierr)
        grid(0, 1:np) = buf_rx(:)
        ! down
        buf_tx(:) = grid(1, 1:np)
        call mpi_sendrecv(buf_tx, np, mpi_double_precision, mp%cart_neighbors(down), mpi_tag, &
                          buf_rx, np, mpi_double_precision, mp%cart_neighbors(up), mpi_tag, &
                          mp%cart_comm, MPI_STATUS_IGNORE, ierr)
        grid(np+1, 1:np) = buf_rx(:)
        ! left
        buf_tx(:) = grid(1:np,1)
        call mpi_sendrecv(buf_tx, np, mpi_double_precision, mp%cart_neighbors(left), mpi_tag, &
                          buf_rx, np, mpi_double_precision, mp%cart_neighbors(right), mpi_tag, &
                          mp%cart_comm, MPI_STATUS_IGNORE, ierr)
        grid(1:np, np+1) = buf_rx(:)
        ! right
        buf_tx(:) = grid(1:np,np)
        call mpi_sendrecv(buf_tx, np, mpi_double_precision, mp%cart_neighbors(right), mpi_tag, &
                          buf_rx, np, mpi_double_precision, mp%cart_neighbors(left), mpi_tag, &
                          mp%cart_comm, MPI_STATUS_IGNORE, ierr)
        grid(1:np, 0) = buf_rx(:)
        deallocate(buf_tx)
        deallocate(buf_rx)
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
    use mpi
    use omp_lib
    use diff2d_mod
    implicit none

    double precision, allocatable, target :: grid_1(:,:), grid_2(:,:)
    double precision, pointer :: grid(:,:), grid_new(:,:), grid_tmp(:,:)
    integer :: fp, i, ix, iy, n_iterations, np
    double precision :: dt, D, t0
    type(mpi_stuff) :: mp
    namelist /diff/ n_iterations, np, dt, D

    open(newunit=fp, file="diff_par.nml", status='old', action='read')
    read(fp, diff)
    close(fp)

    ! column major ordering, y upwards and fastest varying index
    !                    Y,      X
    allocate(grid_1(0:np+1, 0:np+1))
    allocate(grid_2(0:np+1, 0:np+1))

    grid => grid_1
    grid_new => grid_2

    call mpi_setup(mp)
    call initial_condition(grid_1, np)

    t0 = omp_get_wtime()

    do i=1,n_iterations
        call apply_periodic_boundary_conditions(grid, mp, np)
        call evolve(grid, grid_new, np, dt, D)
        grid_tmp => grid_new
        grid_new => grid
        grid => grid_tmp
        if ((modulo(i,100) == 0).and.(mp%world_rank == 0)) &
            write(*,*) int(100.0 * real(i)/real(n_iterations)), "%"
    enddo

    if (mp%world_rank == 0) then
        write(*,*) "main loop time =", omp_get_wtime() - t0
        ! --- final data dump for inspection through Python diagnostics script
        open(newunit=fp, file="/tmp/diff_par.dat", status='replace', action='write')
        do ix=1,np
            do iy=1,np
                write(fp, *) grid(iy,ix)
            enddo
        enddo
        close(fp)
    endif

    deallocate(grid_1)
    deallocate(grid_2)
    call mpi_teardown(mp)
end program diff2d
