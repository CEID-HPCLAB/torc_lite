# Torc‑Lite

Torc‑Lite is a lightweight task-based runtime for MPI applications that provides a master/worker execution model and local multithreading (pthreads). It exposes a small C API to create tasks, synchronize, and exchange data across MPI nodes.

Key goals:
- Provide a compact, portable runtime for task-parallel MPI programs.
- Support multiple POSIX synchronization strategies (mutexes or spinlocks).
- Offer a simple API that integrates with existing MPI applications and Fortran code.

For details and historical notes see the original INSTALL and COPYING files included in the repository.

---

## Features

- Task creation and scheduling via `torc_task` / `torc_create` API.
- Server thread to handle MPI communication and optional non-blocking server.
- Configurable synchronization backends: `mutex`, `mutex_try`, `spin`, `spin_try`.
- Small demo programs illustrating common patterns (async tasks, broadcast, master/slave, benchmarks).
- Optional null-MPI stub (nullmpi/) for builds on systems without MPI.

## Stack
- Language: C (with optional Fortran wrappers)
- Concurrency: POSIX threads (pthreads)
- Message passing: MPI (MPICH / Open MPI expected)
- Build: GNU Autotools (autoconf, automake)

## Quick repository map
```
configure*                 Autotools-generated configure script
configure.ac               Autoconf configuration
Makefile.in, Makefile.am   Top-level build files
src/                       Core runtime sources (torc.c, torc_runtime.c, torc_queue.c, torc_comm.c, torc_server.c, torc_thread.c)
include/                   Public and internal headers (include/torc.h, torc_config.h, torc_internal.h, ...)
demo/                      Example programs (async.c, broadcast.c, fibo.c, masterslave.c, mbench1.c, pipe.c, struct.c, zerolength.c)
scripts/                   configure-generated helper scripts (torc_cflags, torc_libs)
nullmpi/                   Lightweight MPI stub for non-MPI builds
INSTALL, README, COPYING   Documentation, license and install notes
```

How it fits together
- Applications call `torc_init(...)`, register tasks, and create them with `torc_task(...)` / `torc_create(...)`.
- The runtime uses pthreads for local concurrency and a dedicated server thread to mediate MPI messages.
- Task queues and the scheduler (src/torc_queue.c and src/torc_runtime.c) decide task placement; work-stealing can be enabled.

## Build & install (short path)
These commands assume you have a thread-safe MPI (mpicc) available and Autotools present.

```bash
# Bootstrap (if you are developing or the autotools files are not already generated):
# autoreconf -i    # only if modifying configure.ac or missing generated files

# Configure and build (example)
./configure CC=mpicc F77=mpif90
make

# Build demos
cd demo
make

# Optional install
# ./configure --prefix=/opt/torc CC=mpicc F77=mpif90
# make && make install
```

Notes on configure options (see configure.ac for full details):
- --with-sync=mutex|mutex_try|spin|spin_try — choose POSIX synchronization mechanism
- --with-maxnodes=NUM — set maximum MPI processes (default 1024)
- --with-maxvps=NUM — set maximum virtual processors (default 64)
- --with-mpi/--with-mpiincdir/--with-mpilibdir — point to a non-standard MPI installation
- --enable-debug — enable debug build flags

The configure step generates small helper scripts in `scripts/`:
- `scripts/torc_cflags` prints the correct include flags for user programs
- `scripts/torc_libs` prints the correct linker flags (e.g. `-L${prefix}/lib -ltorc -lpthread`)

## Running a demo
Use your MPI launcher (mpirun, mpiexec) with the desired process count. Example:

```bash
mpirun -np 4 ./demo/masterslave
```

If you built and installed the library to a custom prefix, use the generated scripts when compiling an application:

```bash
mpicc `./scripts/torc_cflags` -o myprog myprog.c `./scripts/torc_libs`
```

## API quick reference

See `include/torc.h` for full declarations. Key functions:

- `int torc_init(int argc, char *argv[], int ms);` — initialize the runtime.
- `void torc_task(int queue, void (*f)(), int narg, ...);` — create a task. `torc_create()` is an alias for this function.
- `torc_task_detached()`, `torc_task_ex()`, and `torc_task_direct()` — task-creation variants.
- `void torc_waitall(void);` — wait for outstanding child tasks.
- `void torc_finalize(void);` — shut down the runtime.
- `void torc_broadcast(void *a, long count, MPI_Datatype dtype);` — broadcast data to the MPI processes.


Public API is declared in `include/torc.h` and additional internal helpers live in the `include/` headers.

Functions that may execute on another MPI process must be registered with
`torc_register_task()` on every MPI process. Tasks must be registered in the
same order on every process because the runtime transfers registered-function
IDs between processes. Unregistered functions may only be used for tasks that
are guaranteed to execute locally.


### Creating tasks

`torc_create()` creates an asynchronous child task and is an alias for
`torc_task()`:

```c
torc_create(queue, function, narg,
            count_0, datatype_0, mode_0,
            count_1, datatype_1, mode_1,
            /* ... */
            address_0, address_1 /* ... */);
```

- queue is a global worker ID, or `-1` to let Torc-Lite select a worker.
- narg is the number of task arguments. Each argument is first described by
its element count, MPI datatype, and passing mode. The addresses of all
arguments follow the complete list of argument descriptions.
- The principal passing modes are:
    - `CALL_BY_COP` (`IN`): copy the input when the task is created.
    - `CALL_BY_REF` (`INOUT`): pass the original memory locally, or transfer the
input and copy the updated value back after remote execution.
    - `CALL_BY_RES` (`OUT`): write directly to the original memory locally, or
copy the result back after remote execution.
    - `CALL_BY_PTR` (`IN`): provide pointer-based input without copying changes
back.

Example:

```c
torc_create(-1, slave, 2,
            1, MPI_DOUBLE, CALL_BY_COP,
            1, MPI_DOUBLE, CALL_BY_RES,
            &input, &result);

torc_waitall();
```

Functions that may execute on another MPI process must be registered with
torc_register_task() on every process and in the same order. Memory passed
with CALL_BY_REF or CALL_BY_RES must remain valid until the task completes.
After torc_waitall() returns, all child tasks have completed and their
outputs have been written to the supplied memory.


## Development notes
- For standards-compliant execution, the runtime requires `MPI_THREAD_SERIALIZED` or higher. See “Portability and MPI requirements” below for the tested Linux compatibility behavior.
- Synchronization backend and cache-line size are determined at configure time and written to `include/ps_config.h`.
- The main scheduler and queue logic are in `src/torc_runtime.c` and `src/torc_queue.c`.

### Portability and MPI requirements

#### Task-descriptor mutexes

Each task descriptor contains a POSIX mutex or spinlock used for local
dependency synchronization. Although complete task descriptors are transferred
between MPI processes, a received lock representation is process-local state
and must not be used directly. Torc-Lite discards and reinitializes the lock
locally before a received task is queued or executed.

Reinitializing task locks has been tested successfully on Linux. The current
implementation primarily targets Linux POSIX environments; applications
requiring portability to other operating systems or pthread implementations
should verify this behavior.

#### MPI thread support

For standards-compliant execution, Torc-Lite requires
`MPI_THREAD_SERIALIZED` or `MPI_THREAD_MULTIPLE`. When
`MPI_THREAD_SERIALIZED` is provided, Torc-Lite serializes MPI calls with an
internal communication lock.

Torc-Lite has also been observed to work on Linux with Open MPI and MPICH when
the reported level is `MPI_THREAD_SINGLE`. In that configuration, MPI calls
remain serialized, but calls may originate from different Torc-Lite threads.
This behavior is implementation-specific and is not guaranteed by the MPI
standard.


---

## Example: Simple masterslave program

The following minimal example demonstrates a typical Torc‑Lite program that registers a task, initializes the runtime, creates a set of tasks and waits for their completion. It is a compact version of `demo/masterslave.c` included in this repository.

```c
/* masterslave_example.c
 * Minimal Torc-Lite example: compute square roots in parallel
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <torc.h>

void slave(double *pin, double *out)
{
    double in = *pin;
    /* simulate work */
    sleep(1);
    *out = sqrt(in);
    printf("slave: in=%f out=%f\n", in, *out);
}

int main(int argc, char *argv[])
{
    int n = 4; /* number of tasks */
    double *inputs = malloc(n * sizeof(double));
    double *results = malloc(n * sizeof(double));

    for (int i = 0; i < n; i++) {
        inputs[i] = (double)(i + 1);
        results[i] = 0.0;
    }

    /* Tell the runtime which functions may be invoked as tasks */
    torc_register_task(slave);

    /* Initialize the runtime (MODE_MS selects master/slave mode used in demos) */
    torc_init(argc, argv, MODE_MS);

    /* Optionally enable work stealing for better load balance on many threads */
    torc_enable_stealing();

    /* Create tasks (queue = -1 lets the runtime choose local queue) */
    for (int i = 0; i < n; i++) {
        torc_create(-1, slave, 2,
                    1, MPI_DOUBLE, CALL_BY_COP,
                    1, MPI_DOUBLE, CALL_BY_RES,
                    &inputs[i], &results[i]);
    }

    /* Wait for all tasks to complete */
    torc_waitall();

    /* Print results */
    for (int i = 0; i < n; i++) {
        printf("result[%d] = sqrt(%g) = %g\n", i, inputs[i], results[i]);
    }

    torc_finalize();
    free(inputs);
    free(results);

    return 0;
}
```

Build and run the example (from the repository root):

```bash
# build the library and the demos first (see Build & install above)
# compile the example using the helper scripts generated by configure
mpicc `./scripts/torc_cflags` -o masterslave_example demo/masterslave_example.c `./scripts/torc_libs`

# run with 4 MPI processes
mpirun -np 4 ./masterslave_example
```

Notes:

- The demos in `demo/` provide several more complete examples (async, broadcast, fibo, pipe, etc.).
- See `include/torc.h` for detailed API usage and the demos for realistic patterns and argument passing modes (`CALL_BY_COP`, `CALL_BY_RES`, `CALL_BY_REF`).


## License
Torc-Lite is distributed under the MIT License. See LICENSE for the full license text.
Torc-Lite was developed by Panagiotis E. Hadjidoukas. The project preserves the original copyright and authorship notices.
Third-party components, if any, remain subject to their respective licenses, as documented in their directories.


## Authors / Contact
See the `AUTHORS` file for contributors and historical credits. The repository originally created by Panagiotis Hadjidoukas and collaborators.


## Related publications

**Preferred citation for Torc-Lite**

- P. E. Hadjidoukas, E. Lappas, and V. V. Dimakopoulos, **“A Runtime Library for Platform-Independent Task Parallelism,”** *20th Euromicro International Conference on Parallel, Distributed and Network-Based Processing (PDP)*, pp. 229–236, 2012. [DOI: 10.1109/PDP.2012.89](https://doi.org/10.1109/PDP.2012.89).

**Earlier foundations and subsequent applications/extensions**

- P. E. Hadjidoukas, **“A Lightweight Framework for Executing Task Parallelism on Top of MPI,”** *Recent Advances in Parallel Virtual Machine and Message Passing Interface*, pp. 287–294, 2004. [DOI: 10.1007/978-3-540-30218-6_41](https://doi.org/10.1007/978-3-540-30218-6_41). *(Earlier research on MPI task parallelism.)*
- V. V. Dimakopoulos and P. E. Hadjidoukas, **“HOMPI: A Hybrid Programming Framework for Expressing and Deploying Task-Based Parallelism,”** *Euro-Par 2011*, pp. 14–26, 2011. [DOI: 10.1007/978-3-642-23397-5_3](https://doi.org/10.1007/978-3-642-23397-5_3). *(Task programming environment using TORC as its runtime.)*
- P. E. Hadjidoukas, C. Voglis, V. V. Dimakopoulos, I. E. Lagaris, and D. G. Papageorgiou, **“Supporting Adaptive and Irregular Parallelism for Non-Linear Numerical Optimization,”** *Applied Mathematics and Computation*, vol. 231, pp. 544–559, 2014. [DOI: 10.1016/j.amc.2013.12.092](https://doi.org/10.1016/j.amc.2013.12.092). *(Nested task parallelism and optimization with TORC.)*
- P. E. Hadjidoukas, P. Angelikopoulos, C. Papadimitriou, and P. Koumoutsakos, **“Π4U: A High Performance Computing Framework for Bayesian Uncertainty Quantification of Complex Models,”** *Journal of Computational Physics*, vol. 284, pp. 1–21, 2015. [DOI: 10.1016/j.jcp.2014.12.006](https://doi.org/10.1016/j.jcp.2014.12.006). *(Application framework using TORC.)*
- P. E. Hadjidoukas, A. Bartezzaghi, F. Scheidegger, R. Istrate, C. Bekas, and A. C. I. Malossi, **“torcpy: Supporting Task Parallelism in Python,”** *SoftwareX*, vol. 12, article 100517, 2020. [DOI: 10.1016/j.softx.2020.100517](https://doi.org/10.1016/j.softx.2020.100517). *(Related Python task-parallel runtime software, not an additional paper specifically documenting this C repository.)*

The papers describe related research at different stages and are not interchangeable citations for this specific Torc-Lite codebase. GitHub's **Cite this repository** action uses the PDP 2012 paper specified in [`CITATION.cff`](CITATION.cff).

## Software authorship and acknowledgments

Torc-Lite was authored and developed solely by **Panagiotis E. Hadjidoukas**. **Yaser Afshar** tested the library and provided feedback and suggestions for improvements. Related changes implemented by Afshar in his separate GitHub repository are not code contributions to this repository. See [`AUTHORS`](AUTHORS) for the full attribution.
