# Recursive Fibonacci and nested tasks

The bundled [`demo/fibo.c`](../generated/examples/fibo.md) demonstrates **recursive task creation**. A high-level task recursively creates another task, while one branch executes inline.

```mermaid
flowchart TD
    F[fib(n)] --> A[torc_create fib(n-1)]
    F --> B[inline fib(n-2)]
    A --> J[torc_waitall]
    B --> J
    J --> S[sum branch results]
```

The code switches to ordinary recursive calls for smaller inputs using a threshold based on `FIB_NUM` and `LEVELS`.

## Run

```bash
TORC_WORKERS=4 mpirun -np 1 ./demo/fibo 35
TORC_WORKERS=2 mpirun -np 2 ./demo/fibo 35
```

This example illustrates *how* to use nested parallelism, not an efficient algorithm for computing Fibonacci numbers. The exponential recursion remains inefficient; the purpose is to demonstrate scheduling and joins.

## Lessons

- Spawn useful work, not every tiny recursive call.
- Execute some work locally while children run asynchronously.
- Wait for children before accessing their result buffers.
- Register recursive task functions across ranks.

Related: [nested task programming](../concepts/nested-parallelism.md), [performance](../concepts/performance.md).
