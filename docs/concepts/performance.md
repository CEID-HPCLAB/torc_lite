# Performance and scalability

Torc-Lite provides scheduling mechanisms; parallel efficiency still depends on task characteristics, allocation, and application design. Benchmark **your workload**, not just a synthetic task-creation loop.

## Performance model

Useful quantities are:

- **Work:** total time needed to execute task bodies serially, excluding duplicated work.
- **Span / critical path:** longest dependency chain in a nested task graph.
- **Task overhead:** scheduling, descriptor management, local synchronization, and communication.
- **Load imbalance:** idle time because ready work is unavailable at some workers.
- **Data movement:** cost of transferring remote task arguments and results.

An approximate upper bound for speedup is limited by available task concurrency and by the critical path. Small tasks can suffer from overheads; large tasks offer less flexibility to rebalance.

## Benchmark procedure

1. Define a correct serial baseline and representative input data.
2. Run one MPI process and increase `TORC_WORKERS` gradually.
3. Fix the total number of workers and compare different MPI-rank/worker mappings.
4. Measure with and without task stealing for variable-duration workloads.
5. Record task creation time, total elapsed time, time spent waiting, and runtime variability.
6. Repeat runs; report median and variation along with machine/compiler/MPI details.

## Task overhead microbenchmark

[`demo/mbench1.c`](../generated/examples/mbench1.md) performs repeated runs of task creation and waiting. It reports an average task-time measure, which includes its benchmark's own counting and timer methodology. Do not interpret it as a universal one-task latency: measure on your own compiler and environment.

```bash
TORC_WORKERS=4 mpirun -np 1 ./demo/mbench1 1000
```

## Irregular workloads

For heavy physical-model evaluations, individual task times can vary according to model parameters. The uploaded **2015 Euro-Par article** and **2015 JCP Pi4U paper** study chains of unequal length, variable model cost, and TORC-assisted work redistribution. Their reported speedups belong to **those published applications/hardware systems**, and should not be presented as new measurements of this checkout.

## Coupling external simulation programs

TORC can be part of a larger driver that launches simulations, receives their outputs, and uses the returned values in optimization/inference. External process management, persistent proxy processes and GPU-executed model codes are discussed in the historical papers but **are not standalone generic APIs in `include/torc.h`**. Those capabilities require application or companion-framework implementation.

## Common pitfalls

- Oversubscribing cores with `MPI ranks × TORC workers × OpenMP threads`.
- Very fine tasks and large argument payloads when remote dispatch dominates computation.
- Submitting too little work for the number of workers.
- Mutating shared buffers before an asynchronous task completes.
- Forgetting to set task stealing appropriately when work durations differ.
- Treating runtime statistics from debug builds as directly comparable to optimized builds.
