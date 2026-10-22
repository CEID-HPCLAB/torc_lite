# TorcPy: the related Python runtime

[TorcPy](https://github.com/IBM/torc_py) is a **separate, pure-Python task-parallel implementation** drawing on the TORC model. It is described by Hadjidoukas *et al.* in [SoftwareX 12 (2020), 100517](https://doi.org/10.1016/j.softx.2020.100517).

Both projects employ MPI plus multithreading and task-based execution. The Python package uses `mpi4py`, Python threads and queue primitives to implement a futures-oriented interface; Torc-Lite implements a C runtime using pthreads and MPI.

## Comparing the public interfaces

| Feature | Torc-Lite C | TorcPy Python |
|---|---|---|
| Submit a task | `torc_create(queue, f, narg, ...)` | `torcpy.submit(f, *args, ...)` |
| Join child tasks | `torc_waitall()` | `torcpy.wait()` |
| Result representation | Explicit output arguments / buffers | Future-like object and `result()` |
| Parallel map | Compose a task loop | `torcpy.map()` |
| Nested tasks | Recursive calls to `torc_create()` | Recursive `torcpy.submit()` |
| Process/worker introspection | `torc_node_id()`, `torc_worker_id()` etc. | `torcpy.node_id()`, `torcpy.worker_id()` etc. |
| Interoperation with MPI | C MPI API and runtime rules | `torcpy.spmd()` and mpi4py in documented patterns |
| Argument transfer | MPI datatype/count/mode metadata | Python serialization through TorcPy internals |

**Do not** copy TorcPy API names verbatim into Torc-Lite C code. The overlap is in programming *concepts*, not binary interface or package contents.

## TorcPy example (illustrative Python only)

From the TorcPy documentation's submit/wait idiom:

```python
import torcpy as torc


def work(x):
    return x * x


def main():
    tasks = [torc.submit(work, x) for x in range(10)]
    torc.wait()
    print([task.result() for task in tasks])


if __name__ == "__main__":
    torc.start(main)
```

Torc-Lite C instead declares a task with pointer arguments, submits it with `torc_create()`, waits, and reads the result buffer. See the [first-program guide](../getting-started/first-program.md).

## TorcPy's useful documentation concepts

The TorcPy documentation offers accessible explanations of:

- Asynchronous task submission and completion.
- Hierarchical recursive work, including Fibonacci.
- Worker and MPI-rank addressing.
- Stealing tasks and balancing irregular execution.
- A hybrid MPI/pthreads runtime with communication server threads.

Those conceptual descriptions have helped structure this Torc-Lite site. **Details of actual C runtime calls, argument modes, defaults, and limitations are taken from Torc-Lite sources, not inferred from TorcPy.**

## Resources

- [TorcPy GitHub repository](https://github.com/IBM/torc_py)
- [TorcPy on PyPI](https://pypi.org/project/torcpy/)
- [TorcPy SoftwareX article](https://doi.org/10.1016/j.softx.2020.100517)
