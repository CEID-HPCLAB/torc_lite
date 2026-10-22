# C API reference

Header: [`include/torc.h`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/torc.h). The list below reflects the public header of the checked repository; this is not a promise of stable ABI across unreleased source changes.

## Program lifecycle

| Signature | Purpose |
|---|---|
| `int torc_init(int argc, char *argv[], int ms);` | Initialize runtime; the `MODE_MS` / `MODE_MW` constants select the master–worker mode |
| `void torc_finalize(void);` | End the runtime; historical shutdown modes may end the process |
| `void torc_register_task(void *f);` | Register functions for potential remote execution; ordering must match across ranks |
| `void torc_reset_statistics(void);` | Reset internal statistics |

The canonical startup pattern appears in [master–worker](../examples/masterworker.md). Note that `torc_register_task` is declared as receiving `void *`, while examples pass function identifiers; exact compiler warning behavior depends on compiler/language mode.

## Task submission

```c
void torc_task(int queue, void (*f)(), int narg, ...);
void torc_task_detached(int queue, void (*f)(), int narg, ...);
void torc_task_ex(int queue, int invisible, void (*f)(), int narg, ...);
void torc_task_direct(int queue, void (*f)(), int narg, ...);
```

The public header provides aliases:

```c
#define torc_create          torc_task
#define torc_create_detached torc_task_detached
#define torc_create_ex       torc_task_ex
#define torc_create_direct   torc_task_direct
```

A call specifies a `queue` (a global worker ID or `-1`), callback function, argument count, then `(element count, MPI datatype, passing mode)` for each parameter and finally one address per parameter.

Use ordinary `torc_create()` and `torc_waitall()` for new programs unless an advanced scheduling use case needs another variant.

## Synchronization and execution

| Signature | Meaning / caution |
|---|---|
| `void torc_waitall(void);` | Wait for child tasks created by the caller |
| `void torc_waitall2(void);` | Specialized wait operation used by advanced demos |
| `void torc_waitall3(void);` | Specialized wait operation used by advanced demos |
| `void torc_tasksync(void);` | Task synchronization helper |
| `int torc_scheduler_loop(int once);` | Internal-style scheduler interaction exposed publicly; advanced use only |
| `int torc_fetch_work(void);` | Specialized work retrieval; advanced use only |
| `void torc_taskinit(void);` | Task initialization hook; compatibility/no-op in current C implementation |

`waitall2`, `waitall3`, `scheduler_loop` and `fetch_work` are **not substitutes** for ordinary `torc_waitall()` without first reviewing their source and the examples.

## Worker and process queries

```c
int torc_node_id(void);
int torc_num_nodes(void);
int torc_worker_id(void);
int torc_num_workers(void);
int torc_i_worker_id(void);
int torc_i_num_workers(void);
int torc_getlevel(void);
```

`node` corresponds to an MPI process. `worker` refers to the task runtime. The `i_` query variants access local identities and counts; see [MPI interoperability](../concepts/mpi.md).

## Scheduling control

```c
void torc_enable_stealing(void);
void torc_disable_stealing(void);
void torc_i_enable_stealing(void);
void torc_i_disable_stealing(void);
```

The `i_` variants affect local scheduling and should be used with care in advanced code. `TORC_STEALING` can enable interprocess stealing at initialization.

## Data movement and clocks

```c
void torc_broadcast(void *a, long count, MPI_Datatype dtype);
void torc_broadcast_ox(void *a, long count, int dtype);
typedef double torc_time_t;
torc_time_t torc_gettime(void);
void thread_sleep(int ms);
```

The [broadcast example](../generated/examples/broadcast.md) uses `torc_broadcast()` for scalars and arrays. Use the declared element count and matching MPI datatype.

## Argument modes

```c
#define CALL_BY_COP   1
#define CALL_BY_REF   2
#define CALL_BY_RES   3
#define CALL_BY_PTR   4
#define CALL_BY_VAL   1
#define CALL_BY_COP2  5
#define CALL_BY_VAD   6
```

`CALL_BY_VAL` aliases the numerical value of `CALL_BY_COP`; consult [argument semantics](../concepts/arguments.md) rather than inferring C++ value semantics from its name.

## Environment and build interface

Runtime variables include `TORC_WORKERS`, `TORC_STEALING`, `TORC_YIELDTIME`, `TORC_THROTTLING_FACTOR`, and the fallback `OMP_NUM_THREADS`. Configure-time options define synchronization and maximum supported sizes; read the [configuration guide](../getting-started/configuration.md).
