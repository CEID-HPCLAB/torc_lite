
      program masterslave
      implicit none
c      include 'mpif.h'
      include 'torcf.h'

      integer i
      integer ntasks
      parameter (ntasks = 4)

      double precision input(ntasks), result(ntasks)
      external slave

C     Register the task function
      call torc_register_task(slave)

C     Initialize TORC
      call torc_init(MODE_MS)

C     Enable work stealing
       call torc_enable_stealing()

C     Create 4 asynchronous tasks
      do i = 1, ntasks
         input(i) = dble(i)
         result(i) = -1.0d0

         call torc_create(-1, slave, 2,
     &        1, MPI_DOUBLE_PRECISION, CALL_BY_COP,
     &        1, MPI_DOUBLE_PRECISION, CALL_BY_RES,
     &        input(i), result(i))
      enddo

C     Wait until all tasks have completed
      call torc_waitall()

C     Print the results
      do i = 1, ntasks
         print *, 'sqrt(', input(i), ') = ', result(i)
      enddo

      call torc_finalize()
      end


C     Task function
      subroutine slave(x, y)
      implicit none
      include 'torcf.h'

      double precision x, y

      y = sqrt(x)

      print *, 'Rank ', torc_node_id(),
     &         ': sqrt(', x, ') = ', y

      end
