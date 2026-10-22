# Nested task parallelism

Nested parallelism lets a task generate more child tasks. It is one of the distinguishing features of the TORC family: an irregular application can expose concurrency at multiple levels rather than allocating a fixed, hard-partitioned worker group to each algorithm stage.

## Example: recursive Fibonacci

The repository includes [`demo/fibo.c`](../generated/examples/fibo.md), in which a recursive call conditionally launches another TORC task:

```c
torc_create(-1, slave, 2,
            1, MPI_LONG, CALL_BY_COP,
            1, MPI_LONG, CALL_BY_RES,
            &n_1, &res1);
slave(&n_2, &res2);
torc_waitall();
```

The code computes one branch asynchronously, computes the other branch synchronously, and joins at the end. This exposes parallelism while avoiding unnecessary creation of two tasks for every recursive node.

!!! tip "Use a cutoff"
    Recursive Fibonacci creates many tiny tasks if every recursive call is submitted. The bundled example limits task creation with its `FIB_NUM`/`LEVELS` constants and calculates smaller branches serially. Choose a cutoff based on task cost and the number of allocated workers.

## Waiting inside nested tasks

`torc_waitall()` waits for child tasks associated with the currently executing task. This is different from assuming every task waits for every other task in the application. The runtime can execute ready work while a task is waiting for dependencies.

## Nested model evaluations

A scientific task graph may have three logical levels:

1. Outer inference/optimization iteration.
2. One task per independent chain, candidate solution, or subproblem.
3. Additional tasks for independent simulations, numerical derivatives, or repeated samples.

A model evaluation can also call sequential or thread-parallel code directly instead of spawning extra TORC tasks. For external MPI programs, avoid oversubscribing the same MPI allocation and use the application's orchestration policy rather than assuming a generic `torc_create()` can safely launch arbitrary MPI subjobs.

## Portability of nested tasks

Task functions that might migrate to another MPI rank must be registered everywhere. Lifetime rules and data-passing modes apply **at every nesting level**. See [task arguments](arguments.md), [MPI interoperability](mpi.md) and [the recursive example](../examples/fibonacci.md).
