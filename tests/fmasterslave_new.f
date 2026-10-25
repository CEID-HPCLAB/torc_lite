
      program masterslave
      implicit none
      include 'torcf.h'

      integer ntasks
      parameter (ntasks = 4)

      integer i
      integer quantity(2)
      integer datatype(2)
      integer callway(2)

C     Pointer-sized addresses (64-bit platform).
      integer*8 addresses(2)

      double precision input(ntasks)
      double precision result(ntasks)

      external slave

C     Register task
      call torc_register_task(slave)

C     Initialize TORC
      call torc_init(MODE_MS)

C     Argument descriptors
      quantity(1) = 1
      quantity(2) = 1

      datatype(1) = MPI_DOUBLE_PRECISION
      datatype(2) = MPI_DOUBLE_PRECISION

      callway(1) = CALL_BY_COP
      callway(2) = CALL_BY_RES

C     Create four asynchronous tasks
      do i = 1, ntasks

         input(i) = dble(i)
         result(i) = -1.0d0

C        Addresses of the actual arguments
         addresses(1) = loc(input(i))
         addresses(2) = loc(result(i))

         call torc_create_packed(-1, slave, 2,
     &        quantity, datatype, callway, addresses)

      enddo

C     Wait for completion
      call torc_waitall()

C     Print results
      do i = 1, ntasks
         print *, 'sqrt(', input(i), ') = ', result(i)
      enddo

      call torc_finalize()
      end


      subroutine slave(x, y)
      implicit none

      double precision x, y

      y = sqrt(x)

      end
