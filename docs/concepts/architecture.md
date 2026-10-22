# Runtime architecture

Torc-Lite combines **MPI processes** with **local POSIX worker threads**. The library manages queues of tasks and communicates task descriptors and argument data between MPI processes. An internal server thread handles interprocess communication.

```mermaid
flowchart TD
    subgraph N0[Compute node / MPI process 0]
        M[Primary application task]
        Q0[Task queues by nesting level]
        S0[Communication server thread]
        W00[Worker 0]
        W01[Worker 1]
        M --> Q0
        Q0 --> W00
        Q0 --> W01
        W00 --> Q0
    end
    subgraph N1[MPI process 1]
        Q1[Task queues by nesting level]
        S1[Communication server thread]
        W10[Worker 0]
        W11[Worker 1]
        Q1 --> W10
        Q1 --> W11
    end
    S0 <-->|MPI task/data messages| S1
    Q0 -. Work placement / stealing .-> Q1
```

## Components

| Component | Responsibility | Source |
|---|---|---|
| Application-facing task API | Create tasks, manage argument modes, synchronize | [`src/torc.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc.c) |
| Runtime and scheduler | Execute tasks, synchronization, scheduler loop, statistics | [`src/torc_runtime.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc_runtime.c) |
| Queues and placement | Local queues, target workers and remote queue insertion | [`src/torc_queue.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc_queue.c) |
| MPI communication | Task messages, results, broadcasts, registration | [`src/torc_comm.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc_comm.c) |
| Worker threads | Local pthread creation and worker scheduling | [`src/torc_thread.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc_thread.c) |
| Communication server | Receives and serves task messages / requests | [`src/torc_server.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc_server.c) |

## Task hierarchy

A task can create child tasks, and those child tasks can launch more work. A queued task is detached from the worker that created it: the runtime may execute it on another eligible worker or MPI process.

```mermaid
flowchart TD
    R[Parent application task] --> C1[Chain task A]
    R --> C2[Chain task B]
    C1 --> E11[Model evaluation 1]
    C1 --> E12[Model evaluation 2]
    C2 --> E21[Model evaluation 3]
    C2 --> E22[Model evaluation 4]
```

This is the underlying rationale for multilevel parallelism in **TMCMC and other Pi4U algorithms**. The algorithms are outside the runtime: Torc-Lite does not itself implement TMCMC, Bayesian inference, or CMA-ES. See [research applications](../research/applications.md).

## Historical architecture schematic

![Historical diagram of TORC's MPI processes, worker/server threads, and priority queues](../assets/runtime-architecture-2022.png)

*Historical illustration from Hadjidoukas, “Exploiting Task-Based Parallelism in Bayesian Uncertainty Quantification,” CEID University of Patras presentation (March 2022), slide 15. It illustrates the general TORC runtime concept; consult the current source for the exact behavior of this Torc-Lite checkout.*

## Distinguishing general TORC publications from Torc-Lite

The [PDP 2012 paper](../research/publications.md) and the [2015 Pi4U paper](../research/publications.md) describe the broader TORC programming model and its use at scale. The API, build requirements, and behavior documented elsewhere on **this site** are grounded in the **current CEID-HPCLAB `torc_lite` source**, including differences introduced in later maintenance work.
