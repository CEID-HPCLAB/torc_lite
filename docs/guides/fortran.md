# Using Torc-Lite from Fortran

Torc-Lite includes Fortran-facing declarations and wrappers, but the **bundled example suite is C-focused**. Its Fortran interface uses older compiler conventions (`mpif.h`, fixed-form `torcf.h`, compiler-specific symbol naming), not a published high-level modern Fortran module.

## Build prerequisites

The Autotools configuration supports a Fortran MPI wrapper:

```bash
./configure CC=mpicc F77=mpif90
make
```

Depending on your MPI installation, replace `mpif90` with `mpifort`. Link Fortran applications against the TORC library and its MPI/pthread dependencies using the configured toolchain.

## Interface

The repository's [`include/torcf.h`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/include/torcf.h) provides `MODE_MS`, argument passing constants and `EXTERNAL`/function declarations. The wrapper code in [`src/torc.c`](https://github.com/CEID-HPCLAB/torc_lite/blob/master/src/torc.c) includes `torc_createf`, `torc_taskf`, and `torc_broadcastf`.

The intended pattern parallels the C API: register task functions, initialize the runtime through the appropriate compiler-dependent entry point, submit tasks, wait, and finalize.

!!! warning "Verify symbol naming before porting a large application"
    The original wrappers use Autotools `F77_FUNC_` symbol-name macros. Some wrappers referenced in the Fortran header may differ from the actual exported library symbols in a given build. Verify them with `nm` or a minimal compile/link test first, and confirm the argument descriptors. Do not claim the site has already tested an end-to-end Fortran example on all MPI compilers.

## Source examples in a Fortran-using application

Pi4U includes Fortran-oriented clients and numerical differentiation tools using TORC conventions. Their algorithms are **applications**, not part of Torc-Lite's public runtime interface. Consult [Pi4U](https://github.com/CEID-HPCLAB/pi4u) for integration context.

## Checklist

1. Verify MPI compiler, Fortran symbol naming and `mpif.h` availability.
2. Include the intended Torc-Lite header and confirm the wrapper symbol names.
3. Test the task registration and one `CALL_BY_COP` / `CALL_BY_RES` task.
4. Test on multiple MPI ranks before introducing nested work or derived types.
