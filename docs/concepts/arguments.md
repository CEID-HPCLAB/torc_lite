# Task arguments and data movement

Torc-Lite describes task arguments using MPI datatypes and argument-passing modes. This makes it possible to schedule the same task locally or on a remote MPI process without application-level send/receive code for each value.

## Argument declaration layout

```c
torc_create(target, function, narg,
            count0, mpi_dtype0, passing_mode0,
            count1, mpi_dtype1, passing_mode1,
            /* ... one descriptor triple per argument ... */
            &arg0, &arg1 /* addresses are listed last */);
```

For `narg = 2`, the call accepts **two triples followed by two addresses**. The function receives one pointer per argument.

## Passing modes

| C constant | Typical intent | Behavior to consider |
|---|---|---|
| `CALL_BY_COP` | Input (`IN`) | Capture a copy of an input value at task submission; no write-back |
| `CALL_BY_REF` | Input/output (`INOUT`) | Provide input; copy modifications back when a task finishes remotely; may reference original storage locally |
| `CALL_BY_RES` | Output (`OUT`) | Store returned output in the original address; remote execution copies result back |
| `CALL_BY_PTR` | Pointer-based input | Special pointer mode; do not assume raw pointer addresses are valid across MPI processes |
| `CALL_BY_VAL` | Historical alias for mode value `1` | Source marks different C/Fortran conventions; use with a compatible task signature |
| `CALL_BY_COP2`, `CALL_BY_VAD` | Additional specialized modes | Check implementation and Fortran wrappers before adopting |

The constants are declared in [`include/torc.h`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/torc.h). The source-backed examples use mostly `CALL_BY_COP`, `CALL_BY_RES`, and `CALL_BY_REF`.

## Example: input and output scalars

```c
void square(double *x, double *y) { *y = (*x) * (*x); }

/* Inside an initialized Torc-Lite application */
double x = 3.0;
double y = 0.0;
torc_create(-1, square, 2,
            1, MPI_DOUBLE, CALL_BY_COP,
            1, MPI_DOUBLE, CALL_BY_RES,
            &x, &y);
torc_waitall();
/* y is now 9.0 */
```

### Copy semantics versus output semantics

`CALL_BY_COP` allows the caller to reuse the input variable after submission, since the library captures the necessary input. In contrast, an output buffer supplied through `CALL_BY_RES` or `CALL_BY_REF` must remain available until the task's completion.

## Arrays

```c
double values[8] = {0};
torc_create(-1, work, 1,
            8, MPI_DOUBLE, CALL_BY_REF,
            values);
torc_waitall();
```

On a remote rank, array data are serialized using the declared count and MPI datatype. The application must ensure the declared `count` agrees with the size of allocated memory.

## Structures

The bundled [`struct.c`](../generated/examples/struct.md) passes a C struct through an MPI primitive datatype and `CALL_BY_REF`. The source uses `sizeof(struct tdata) / sizeof(long)` units. This assumes appropriate size/alignment and representation; for heterogeneous machines or production applications, prefer a defined MPI datatype or an explicit serialization format rather than relying on struct memory layout.

## Zero-length buffers

The bundled [`zerolength.c`](../generated/examples/zerolength.md) tests a task argument with a zero element count and a `NULL` pointer. Recent Torc-Lite changes validate argument count/quantity and MPI datatype sizes. Treat zero-sized buffers as a special case worth testing on your MPI implementation.

## Safety checklist

- Register remotely executable functions consistently across ranks.
- Use the correct `MPI_Datatype` and element count for each argument.
- Ensure result buffers remain alive through `torc_waitall()`.
- Avoid sharing writable local memory across concurrent tasks without synchronization.
- Do not use process-local pointer values to refer to memory in another MPI process.
