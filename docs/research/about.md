# Authorship, maintenance, and project history

**Torc-Lite** is the C-based lightweight TORC runtime. Its principal and sole code developer is **Panagiotis E. Hadjidoukas**, now maintaining the project at **CEID-HPCLAB, University of Patras, Greece**.

The repository's `AUTHORS` file also acknowledges **Yaser Afshar** for testing and suggesting improvements. His related development work was carried out in a separate repository, rather than as code contributions to this Torc-Lite repository.

## History

The broader TORC work is described in the PDP 2012 publication. Torc-Lite source headers identify development beginning in the original academic period. The source repository was subsequently moved into GitHub and is now maintained at:

**[github.com/CEID-HPCLAB/torc_lite](https://github.com/CEID-HPCLAB/torc_lite)**.

The checked-out source includes C runtime components, a Fortran compatibility interface, demos, and GNU Autotools build files. Current maintenance has addressed argument validation, runtime synchronization and portability issues.

## Licensing notes

At the time this website was prepared, the repository contained **both an MIT `LICENSE` and a GPLv3 `COPYING` at the root**, plus separate GPLv2 material in the `nullmpi/` subtree. These conflicting files require a project-level licensing decision and review of component ownership before the site can state a definitive blanket MIT license for all bundled files.

Check the [live repository license files](https://github.com/CEID-HPCLAB/torc_lite) for current terms; the documentation package does **not** modify licensing or copyright notices.

## Connections

- [Pi4U](https://github.com/CEID-HPCLAB/pi4u) — task-parallel uncertainty quantification and optimization applications.
- [TorcPy](https://github.com/IBM/torc_py) — independently implemented Python-based TORC programming model.
- [PDP 2012 and related publications](publications.md) — scholarly references.

Issues and code contributions should be submitted through [GitHub Issues](https://github.com/CEID-HPCLAB/torc_lite/issues) or pull requests after reviewing the active repository.
