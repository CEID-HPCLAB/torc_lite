# Data exchange, broadcasts, and structs

## Broadcasting values

[`demo/broadcast.c`](../generated/examples/broadcast.md) demonstrates scalar and array broadcasts from the primary application context:

```c
torc_broadcast(&gi,   1, MPI_INT);
torc_broadcast(&gd,   1, MPI_DOUBLE);
torc_broadcast(&gti, 16, MPI_INT);
torc_broadcast(&gtd, 16, MPI_DOUBLE);
```

After the broadcast, tasks read the updated scalar/array variables. The example is useful for initializing model parameters shared by the application before a parallel stage. Avoid assuming a broadcast has automatically synchronized arbitrary user-level shared memory between independent processes.

## Structure in/out

[`demo/struct.c`](../generated/examples/struct.md) puts an input scalar, an output scalar and a text buffer inside a C structure, then submits the struct as a `CALL_BY_REF` argument. The task modifies the structure and its separate output scalar.

The original demo describes its struct as a number of `MPI_LONG` elements. This can depend on struct representation and architecture: do not treat that as a portable serialization format. Production applications should send explicitly declared primitive fields, derived MPI datatypes, or serialized buffers.

## Zero-length arrays

[`demo/zerolength.c`](../generated/examples/zerolength.md) creates a task with an array argument whose count may be zero. When size is zero, the source passes a `NULL` pointer for the payload; otherwise, it allocates an array, returns task-written values, then prints them.

```bash
TORC_WORKERS=2 mpirun -np 1 ./demo/zerolength 0
TORC_WORKERS=2 mpirun -np 1 ./demo/zerolength 8
```

The example is useful for testing argument edge cases after changing compilers or MPI implementations.

For the semantics of the passing modes, see [arguments and data movement](../concepts/arguments.md).
