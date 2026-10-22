# MPI interoperability and threads

Torc-Lite is built on MPI and pthreads; MPI is part of the **runtime implementation**, not just an optional transport. A typical application launches with `mpirun` or `mpiexec`, and each process hosts one or more task workers.

## MPI rank vs TORC worker

- `torc_node_id()` returns the rank of the current MPI process in the Torc-Lite execution environment.
- `torc_num_nodes()` returns the MPI process count.
- `torc_worker_id()` identifies the calling worker globally when multiple ranks are active.
- `torc_num_workers()` provides the number of workers in the combined execution environment; `torc_i_num_workers()` is the local process worker count.

Example:

```c
printf("MPI rank %d of %d, worker %d of %d\n",
       torc_node_id(), torc_num_nodes(),
       torc_worker_id(), torc_num_workers());
```

## MPI thread levels

The Torc-Lite README specifies that portable operation requires at least `MPI_THREAD_SERIALIZED`. `MPI_THREAD_MULTIPLE` may also be used. The runtime has a communication lock when MPI calls must be serialized.

A MPI library reporting `MPI_THREAD_SINGLE` cannot be assumed safe for runtime calls originating from more than one thread, even if some versions of Open MPI or MPICH happen to work in Linux tests.

## MPI within task functions

The original TORC publications discuss using sequential, OpenMP-parallel, or external MPI codes inside application tasks. **These are application-level coupling patterns.** Avoid concurrent arbitrary calls into the same MPI communicator without understanding the MPI thread support, collective call order, and runtime protocol.

For an application that needs explicit MPI collectives between task phases, the bundled [`pipe.c`](../generated/examples/pipe.md) demonstrates an advanced hybrid arrangement using MPI initialization, pthreads and TORC scheduling. It is a study example, not the recommended first program.

## Task registration across processes

Each task function that could execute on a remote MPI rank must be registered with `torc_register_task()` on every rank in an identical order. The runtime transports function registration IDs rather than transmitting machine code.

## Portability and process-local state

Pthread mutexes and raw pointers cannot be meaningfully transferred between independent processes. Current Torc-Lite code handles some task descriptor state specially when receiving remote tasks; application argument data must likewise be passed using declared MPI datatypes or deliberate serialization.

See the [official README](https://github.com/CEID-HPCLAB/torc_lite/blob/master/README.md) for the current Linux-specific task descriptor note.
