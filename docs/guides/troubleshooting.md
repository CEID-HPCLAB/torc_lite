# Troubleshooting

## `mpicc` / `mpif90` not found

Install an MPI implementation and use the correct compiler wrappers on `PATH`. Some MPI distributions provide `mpifort` rather than `mpif90`.

## Missing generated build files

Regenerate Autotools output when required:

```bash
autoreconf -fi
./configure CC=mpicc F77=mpif90
make
```

## MPI thread-level or deadlock problems

Confirm the MPI implementation provides a thread level compatible with the runtime. The README requires `MPI_THREAD_SERIALIZED` or better for standards-compliant operation. Check collective participation if using the advanced `pipe.c` example or combining the runtime with application-level MPI calls.

## Remote task rejected as unregistered

Register remotely executable task functions on every MPI process, consistently and in the same order, before dispatch. The runtime's communication code rejects unregistered remote task functions.

## Incorrect results / memory corruption

Verify all descriptor triples, MPI datatypes, element counts and buffer lifetimes. Make sure `CALL_BY_RES` and `CALL_BY_REF` addresses remain valid until the task completes. Test first on one rank, then multiple ranks.

## Too many worker threads

Set `TORC_WORKERS` explicitly and compare against `--with-maxvps` limits configured at build time. The runtime validates worker counts and may reject an invalid value. Consider extra OpenMP or simulation-code threads to avoid oversubscription.

## Poor scaling

Check task size, number of submitted tasks, load imbalance, and transfer overhead. Compare with and without task stealing. Run the `mbench1` microbenchmark only as a secondary diagnostic; real application traces matter more.

## Build succeeds but Fortran call fails to link

Inspect exported symbols (e.g. `nm` on `libtorc.a`) and compiler name-mangling conventions, then compare with `F77_FUNC_` wrappers in the source. The Fortran header is historical, so verify before scaling up.

## Documentation site does not publish

1. Repository Settings → Pages → **Build and deployment → Source: GitHub Actions**.
2. Confirm the `Publish Torc-Lite documentation` workflow ran on the `master` branch.
3. Check the `mkdocs build --strict` step and the `actions/deploy-pages` step.
4. Ensure the overlay was added to the repository containing `demo/*.c`; the source-page generator requires these files.
5. Confirm `site_url` in `mkdocs.yml` matches the GitHub Pages path exactly.

If the problem persists, open an issue with OS/compiler/MPI versions, the exact build/run commands, and relevant output: [Torc-Lite issues](https://github.com/CEID-HPCLAB/torc_lite/issues).
