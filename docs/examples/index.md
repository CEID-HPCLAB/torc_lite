# Examples

The repository includes eight C demos. The narrative guides below explain their concepts, while the **source listing pages are regenerated from the current checked-out C files** each time GitHub Pages builds.

| Example | Primary concept | Walkthrough / exact source |
|---|---|---|
| `masterslave.c` | Task creation, scalar argument passing and results | [Guide](masterworker.md) · [Source](../generated/examples/masterslave.md) |
| `fibo.c` | Nested recursive tasks, cutoff, joins | [Guide](fibonacci.md) · [Source](../generated/examples/fibo.md) |
| `broadcast.c` | Broadcast scalars and arrays before tasks | [Guide](data.md) · [Source](../generated/examples/broadcast.md) |
| `struct.c` | Struct input/output with `CALL_BY_REF` | [Guide](data.md) · [Source](../generated/examples/struct.md) |
| `zerolength.c` | Zero-element task arguments | [Guide](data.md) · [Source](../generated/examples/zerolength.md) |
| `async.c` | Detached tasks, callbacks, direct tasks | [Guide](advanced.md) · [Source](../generated/examples/async.md) |
| `pipe.c` | Advanced MPI/pthreads/dispatch interactions | [Guide](advanced.md) · [Source](../generated/examples/pipe.md) |
| `mbench1.c` | Task overhead microbenchmark | [Guide](advanced.md) · [Source](../generated/examples/mbench1.md) |

## Compile and run

```bash
./configure CC=mpicc F77=mpif90
make
cd demo && make && cd ..

TORC_WORKERS=2 mpirun -np 1 ./demo/masterslave
TORC_WORKERS=2 mpirun -np 2 ./demo/masterslave
```

Start with one rank and a small number of workers before running nested or asynchronous examples across multiple MPI ranks.

!!! note "Generated source"
    [`docs/generate_reference.py`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/docs/generate_reference.py) reads the examples from `demo/*.c` at build time, so each documentation build tracks code changes without copy-pasted source duplication.
