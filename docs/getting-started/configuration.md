# Build options and environment variables

Torc-Lite uses two types of configuration: Autotools options decided at **build/configure time**, and variables or API calls that affect **runtime behavior**.

## Selected configure options

| Option | Effect |
|---|---|
| `--prefix=DIR` | Installation prefix; used in generated compiler/linker helper scripts |
| `--with-sync=mutex` | POSIX mutex locking |
| `--with-sync=mutex_try` | Mutex trylock strategy; currently the source's default |
| `--with-sync=spin` | POSIX spinlock locking, when supported |
| `--with-sync=spin_try` | Spinlock trylock strategy |
| `--with-maxnodes=N` | Compile-time maximum MPI processes; default in `configure.ac`: 1024 |
| `--with-maxvps=N` | Compile-time maximum virtual processors/worker slots; default: 64 |
| `--with-cachelinesize=N` | Cache-line size used for configured synchronization/data structures |
| `--enable-debug` | Debug-oriented compilation settings |
| `--with-mpi=DIR` | Nonstandard MPI installation prefix |
| `--with-mpiincdir=DIR` | Explicit MPI header location |
| `--with-mpilib=NAME` | Explicit MPI library name |

The authoritative source is [`configure.ac`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/configure.ac). The value of each compile-time upper bound is **not** an automatic reservation of cores or MPI ranks.

## Runtime environment

The following names appear in the current `src/torc_runtime.c` initialization logic:

| Variable | Meaning |
|---|---|
| `TORC_WORKERS` | Positive number of local worker threads per MPI process; takes precedence over `OMP_NUM_THREADS` |
| `OMP_NUM_THREADS` | Fallback worker-count setting when `TORC_WORKERS` is not set |
| `TORC_STEALING` | Positive value enables interprocess task stealing at startup |
| `TORC_YIELDTIME` | Runtime yielding parameter, for advanced tuning |
| `TORC_THROTTLING_FACTOR` | Advanced throttling parameter; leave unset unless testing a specific configuration |

Example:

```bash
export TORC_WORKERS=4
export TORC_STEALING=1
mpirun -np 2 ./demo/masterslave
```

The number of available workers for applications depends on both the MPI process count and the worker count. Check `torc_num_workers()` rather than assuming every process has the same configuration in all deployments.

## Selecting reasonable worker counts

A useful starting point is one TORC worker per CPU core allocated to the application, **minus threads needed by the application or external models**. Beware of oversubscription when task functions also use OpenMP or spawn parallel programs. MPI process placement, NUMA locality and thread affinity are controlled by the MPI launcher/operating system rather than by a universal Torc-Lite policy.

For a detailed discussion see [performance](../concepts/performance.md).
