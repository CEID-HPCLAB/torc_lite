# Installation

## Requirements

- A Linux or other POSIX-like development environment; **Linux is the primary tested target** in the repository README.
- A C compiler and an MPI implementation providing `mpicc` and an MPI launcher such as `mpirun` or `mpiexec`.
- POSIX threads (`pthreads`).
- A Fortran compiler / `mpif90` for the bundled Autotools configuration and Fortran support.
- GNU Make; Autoconf and Automake if Autotools-generated files need rebuilding.

!!! warning "MPI thread support"
    Standards-compliant operation needs **`MPI_THREAD_SERIALIZED` or better**. The current README reports that some Linux MPICH/Open MPI setups also happen to work when they report `MPI_THREAD_SINGLE`, but that arrangement is not portable under the MPI standard. See [MPI interoperability](../concepts/mpi.md).

## Get the code and build

```bash
# Clone the actively maintained runtime
git clone https://github.com/CEID-HPCLAB/torc_lite.git
cd torc_lite

# Use the provided configure script when present.
./configure CC=mpicc F77=mpif90
make

# Build bundled demos (if not already built at the top level)
cd demo
make
cd ..
```

If the generated `configure` file is absent, or you modified `configure.ac` or `Makefile.am`, regenerate the build system first:

```bash
autoreconf -fi
./configure CC=mpicc F77=mpif90
make
```

Depending on the MPI distribution, the Fortran wrapper might be called `mpifort` rather than `mpif90`:

```bash
./configure CC=mpicc F77=mpifort
```

## Quick smoke test

```bash
# Two TORC workers in a single MPI process
TORC_WORKERS=2 mpirun -np 1 ./demo/masterslave

# Two MPI processes, two local workers each
TORC_WORKERS=2 mpirun -np 2 ./demo/masterslave
```

The demo computes square roots of four inputs. Output order may vary because tasks execute asynchronously. `torc_waitall()` guarantees the results are available before the driver prints them.

!!! note "Launcher environment propagation"
    Your MPI launcher must propagate `TORC_WORKERS` to the target processes. Most local launchers inherit exported environment variables. On managed clusters, consult the scheduler/MPI launch documentation for its preferred syntax.

## Install to a prefix

```bash
./configure --prefix="$HOME/.local/torc" CC=mpicc F77=mpif90
make
make install
export PATH="$HOME/.local/torc/bin:$PATH"
```

The installed helper scripts `torc_cflags` and `torc_libs` expose header and linker arguments. After installation, an application can be built with:

```bash
mpicc $(torc_cflags) -o my_program my_program.c $(torc_libs) -lm
```

The explicit `-lm` is only needed if your application uses math library functions (as the square-root demo does). Without installing, use appropriate source/build paths as needed.

## Platform notes

- Torc-Lite's main implementation is C with pthreads and MPI; it is not a GPU runtime. Tasks can **invoke** programs that use accelerators, but GPU execution is not implemented directly by the Torc-Lite scheduler.
- A bundled `nullmpi/` subtree exists for specialized builds without a full MPI installation. It is not the default or recommended HPC build and has separate historical licensing material.
- The README describes portability considerations when received task descriptors contain process-local mutex state. Validate unusual POSIX/MPI environments before production use.

Next: [your first Torc-Lite program](first-program.md).
