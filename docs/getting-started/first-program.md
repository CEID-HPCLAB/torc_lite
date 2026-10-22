# Your first Torc-Lite program

The bundled [`demo/masterslave.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/demo/masterslave.c) is the canonical starter. Its task computes a square root from a copied input and returns the result through an output argument.

## 1. Task function

```c
void slave(double *pin, double *out)
{
    *out = sqrt(*pin);
}
```

The task receives **pointers**, including for scalar values, because the runtime handles argument payloads using MPI datatypes and passing modes.

## 2. Registration and initialization

```c
torc_register_task(slave);
torc_init(argc, argv, MODE_MS);
```

For remote execution, a task function must be registered on **every MPI process in the same order**. The initialization routine starts the Torc-Lite runtime. In `MODE_MS` (also named `MODE_MW`), rank 0 runs the primary application while other MPI processes serve worker tasks.

## 3. Submit tasks and wait for results

```c
double inputs[4]  = {1.0, 2.0, 3.0, 4.0};
double outputs[4] = {0.0};

for (int i = 0; i < 4; ++i) {
    torc_create(-1, slave, 2,
                1, MPI_DOUBLE, CALL_BY_COP,
                1, MPI_DOUBLE, CALL_BY_RES,
                &inputs[i], &outputs[i]);
}

torc_waitall();

for (int i = 0; i < 4; ++i)
    printf("sqrt(%g) = %g\n", inputs[i], outputs[i]);
```

`-1` requests automatic task placement. `CALL_BY_COP` copies the input at submission time. `CALL_BY_RES` transfers the task result back to the original output location when the task completes. **Both buffers must remain valid until `torc_waitall()` returns.**

The built-in demo uses a local scalar `di` with `CALL_BY_COP` and an output array with `CALL_BY_RES`, illustrating the same contract.

## 4. Full run

After completing [installation](installation.md):

```bash
TORC_WORKERS=2 mpirun -np 1 ./demo/masterslave
TORC_WORKERS=2 mpirun -np 2 ./demo/masterslave
```

There is no guarantee of task print ordering. With variable-duration tasks, try enabling `torc_enable_stealing()` before submission to allow redistribution across MPI processes.

Read the [complete live source](../generated/examples/masterslave.md), [argument semantics](../concepts/arguments.md), and [lifecycle guide](../concepts/lifecycle.md).
