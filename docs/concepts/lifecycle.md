# Program lifecycle

A typical Torc-Lite master–worker program follows this lifecycle:

```mermaid
flowchart LR
    REG[Register functions] --> INIT[torc_init]
    INIT --> SUBMIT[Submit tasks]
    SUBMIT --> WAIT[torc_waitall]
    WAIT --> READ[Read results]
    READ --> FINAL[torc_finalize]
```

## Registration

```c
torc_register_task(work);
```

Torc-Lite transfers **registered-function IDs** between MPI processes rather than assuming function-pointer addresses are meaningful on another rank. Register any remotely executable function on every process, in the same order. Registration before `torc_init()` is the convention in bundled demos.

## Initialization

```c
int status = torc_init(argc, argv, MODE_MS);
```

The current C header defines both `MODE_MS` and `MODE_MW` as `0`, denoting the master–worker startup arrangement. Check the return value where your application needs controlled initialization error handling.

## Asynchronous creation

```c
torc_create(-1, work, 2,
            1, MPI_DOUBLE, CALL_BY_COP,
            1, MPI_DOUBLE, CALL_BY_RES,
            &input, &result);
```

Task calls specify the target queue/worker, function, number of parameters, argument descriptors, then argument addresses. The call enqueues work; it is **not** a synchronous function call. See [arguments](arguments.md).

## Synchronization and result lifetimes

```c
torc_waitall();
/* Read result only after all relevant child tasks finish. */
```

`torc_waitall()` waits for child tasks created by the current task. The runtime can use a waiting worker to execute other queued tasks. This allows nested task graphs to make progress without blocking a physical thread for the duration of every child task.

!!! warning "No early reuse of result buffers"
    Input/output addresses must remain valid until the relevant asynchronous work has finished. In particular, do not return from a function or release memory that is used by outstanding `CALL_BY_REF` or `CALL_BY_RES` tasks.

## Finalization

```c
torc_finalize();
```

In the bundled demos finalization is performed at the end of the application's primary work. Depending on Torc-Lite shutdown options, the runtime may terminate execution instead of returning like an ordinary library function; follow the [`demo/masterslave.c`](../generated/examples/masterslave.md) pattern and its `TORC_NOEXIT` comment.

## Advanced variants

Torc-Lite also exposes detached (`torc_create_detached`), direct (`torc_create_direct`), and other task APIs. Their semantics involve additional scheduling and lifetime considerations; study [advanced examples](../examples/advanced.md) and the [C reference](../api/c.md) before use.
