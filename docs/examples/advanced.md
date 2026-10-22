# Advanced and experimental examples

The following examples explore lower-level runtime operations. **Do not use them as starter templates without understanding their control flow.**

## Asynchronous detached tasks (`async.c`)

[`demo/async.c`](../generated/examples/async.md) uses `torc_create_detached()`, callbacks, completion counts and task creation from a callback. Its task `slave` computes a square root and reports results; callback code maintains a result array and may dispatch more work.

This example shows why detached-task lifetime and data ownership require care. A callback is **not a Python Future callback** and must observe the C runtime's synchronization constraints. The source explicitly avoids ordinary task spawning from its server-thread callback context and uses detached/direct calls instead.

## Mixed pipeline (`pipe.c`)

[`demo/pipe.c`](../generated/examples/pipe.md) includes MPI collectives, a POSIX thread that initializes the runtime, and special wait/scheduler methods. It illustrates coordination across parallel models; it is **not** a drop-in MPI collective recipe. Run only with a thread-aware MPI and after understanding collective participation.

## Microbenchmark (`mbench1.c`)

[`demo/mbench1.c`](../generated/examples/mbench1.md) creates batches of small tasks and estimates creation/completion overhead using `torc_gettime()`.

```bash
TORC_WORKERS=2 mpirun -np 1 ./demo/mbench1 1000
```

Results depend strongly on compiler optimization, MPI configuration, hardware and other system activity. A low microbenchmark overhead does not necessarily predict high efficiency in a communication-heavy nested application.

## Further reading

- [C API reference](../api/c.md)
- [Scheduling and work stealing](../concepts/scheduling.md)
- [MPI interoperability](../concepts/mpi.md)
