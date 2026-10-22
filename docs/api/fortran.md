# Fortran interface reference

Header: [`include/torcf.h`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/torcf.h), which includes `mpif.h`. Torc-Lite provides wrappers in [`src/torc.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc.c).

## Constants

```fortran
      INCLUDE 'torcf.h'
C     MODE_MS is zero for master-worker mode
C     Data movement:
C       CALL_BY_COP = 1
C       CALL_BY_REF = 2
C       CALL_BY_RES = 3
```

The header also defines `CALL_BY_PTR`, `CALL_BY_VAL`, `CALL_BY_COP2` and `CALL_BY_VAD`.

## Declared entry points

Selected names declared or referenced in `torcf.h`:

| Name | Purpose |
|---|---|
| `torc_initf` | Fortran-facing startup helper; verify its availability against the linked library |
| `torc_createf` | Create a child task with descriptor arguments |
| `torc_taskf` | Specialized task creation wrapper used in the parallel differentiation code |
| `torc_register_task` | Register a callable task routine |
| `torc_waitall` | Join child tasks |
| `torc_finalize` | End the runtime |
| `torc_broadcastf` | Broadcast data using an MPI Fortran datatype |
| `torc_worker_id`, `torc_num_workers` | Worker queries |
| `torc_node_id`, `torc_num_nodes` | MPI process queries |
| `torc_gettime` | Wall clock timer |

!!! warning "Wrapper completeness and ABI"
    `torcf.h` is an **interface declaration**, not a complete independently tested Fortran example. Some wrappers use compiler-specific name-mangling macros and `torc_initf` is named in the header but should be verified in the specific source/build. Do not assume modern `ISO_C_BINDING` interfaces exist. See the [Fortran guide](../guides/fortran.md).

## Build and use

Compile/link with the configured MPI Fortran compiler and the installed TORC helper flags, ensuring both the Fortran compiler and the library agree on symbol conventions. See [installation](../getting-started/installation.md).
