# API reference

The authoritative C API is defined in [`include/torc.h`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/torc.h). The associated fixed-form Fortran declaration header is [`include/torcf.h`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/torcf.h).

| Audience | Reference |
|---|---|
| C/C++ caller | [C API](c.md): initialization, submission, synchronization, queries, controls |
| Fortran caller | [Fortran interface](fortran.md): constants, wrappers, calling conventions |

!!! warning "Source API versus TorcPy"
    TorcPy's Python `submit()`, `map()` and `Future` API are **not** declared by Torc-Lite. See the [TorcPy comparison](../research/torcpy.md).

The reference distinguishes common stable patterns used by the demos from specialized APIs whose constraints must be investigated in the implementation.

## Live headers

- [C public header, generated from source](../generated/headers/torc.md)
- [Fortran declaration header, generated from source](../generated/headers/torcf.md)
