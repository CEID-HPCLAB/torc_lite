# From serial loops to task parallelism

A common computational pattern is to evaluate an expensive function independently for many inputs and aggregate the results.

## Serial C

```c
for (int i = 0; i < n; ++i)
    result[i] = evaluate(input[i]);
```

## Torc-Lite task loop

Create a wrapper accepting pointer-based parameters:

```c
void evaluate_task(double *x, double *y)
{
    *y = evaluate(*x);
}
```

In the initialized primary application task:

```c
torc_register_task(evaluate_task);  /* before torc_init */
torc_init(argc, argv, MODE_MS);

for (int i = 0; i < n; ++i)
    torc_create(-1, evaluate_task, 2,
                1, MPI_DOUBLE, CALL_BY_COP,
                1, MPI_DOUBLE, CALL_BY_RES,
                &input[i], &result[i]);

torc_waitall();

/* use result[] */
torc_finalize();
```

The registration and initialization calls belong to the program setup, not repeated inside the evaluation loop. Each output element is a distinct buffer, preventing tasks from overwriting one another's results.

## Adding nested work

If `evaluate()` itself executes independent simulations, consider submitting nested tasks inside `evaluate_task()`. This increases concurrency but also creates more descriptors and possible MPI communication. Keep the subtask cutoff large enough for runtime overhead to remain a small fraction of useful computation.

## For existing OpenMP codes

OpenMP `parallel for` and TORC tasks are complementary. TORC provides a distribution layer across MPI processes; OpenMP may remain inside an evaluation task. Budget workers and OpenMP threads so the combined model does not oversubscribe CPU resources.

## Compared with TorcPy

TorcPy's `submit()`/`wait()` or `map()` patterns express the same general *idea* but use Python callables and Future-style results. Torc-Lite C uses declared counts, MPI datatypes and explicit output-buffer pointers. See [TorcPy comparison](../research/torcpy.md).
