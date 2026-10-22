# Publications

This page distinguishes the primary publication describing **TORC's runtime model** from later papers using TORC or exploring related implementations.

## Preferred runtime citation

**P. E. Hadjidoukas, E. Lappas, V. V. Dimakopoulos.** “A Runtime Library for Platform-Independent Task Parallelism.” *20th Euromicro International Conference on Parallel, Distributed and Network-Based Processing (PDP)*, pp. 229–236, 2012.

[DOI: 10.1109/PDP.2012.89](https://doi.org/10.1109/PDP.2012.89)

The three authors above are the **publication authors**. Torc-Lite's code is authored and maintained by Panagiotis E. Hadjidoukas. Publication authorship is not identical to direct source-code authorship.

## Related TORC and application papers

### Bayesian inference and task-based HPC

**P. E. Hadjidoukas, P. Angelikopoulos, C. Papadimitriou, P. Koumoutsakos.** “Π4U: A high performance computing framework for Bayesian uncertainty quantification of complex models.” *Journal of Computational Physics* **284**, 1–21 (2015). [DOI: 10.1016/j.jcp.2014.12.006](https://doi.org/10.1016/j.jcp.2014.12.006).

The paper describes Pi4U's nonintrusive Bayesian formulation, algorithms, model coupling, nested task graphs and TORC scheduling mechanisms. Its experimental case studies include molecular dynamics, structural dynamics and granular models. [Uploaded source: `pi4u_paper.pdf`.]

**P. E. Hadjidoukas, P. Angelikopoulos, L. Kulakova, C. Papadimitriou, P. Koumoutsakos.** “Exploiting Task-Based Parallelism in Bayesian Uncertainty Quantification.” *Euro-Par 2015*, LNCS **9233**, 532–544. [DOI: 10.1007/978-3-662-48096-0_41](https://doi.org/10.1007/978-3-662-48096-0_41).

This conference paper reports on task-parallel TMCMC, CMA-ES, numerical differentiation and ABC-SubSim, including load-balancing challenges for expensive model evaluations on multicore and hybrid clusters. [Uploaded source: the Springer Nature article PDF.]

### Python implementation

**P. E. Hadjidoukas, A. Bartezzaghi, F. Scheidegger, R. Istrate, C. Bekas, A. C. I. Malossi.** “torcpy: Supporting task parallelism in Python.” *SoftwareX* **12**, 100517 (2020). [DOI: 10.1016/j.softx.2020.100517](https://doi.org/10.1016/j.softx.2020.100517).

TorcPy adopts the TORC concepts using Python's MPI/multithreading ecosystem and a Future-like programming interface. It is related research, **not the same software as Torc-Lite**.

### Optimization and runtime research

**P. E. Hadjidoukas and collaborators.** “Supporting Adaptive and Irregular Parallelism for Non-Linear Numerical Optimization.” *Applied Mathematics and Computation* (2014). [DOI: 10.1016/j.amc.2013.12.092](https://doi.org/10.1016/j.amc.2013.12.092).

This is further background on adaptive/irregular task parallelism. Consult the linked publication for the full bibliographic record and algorithm-specific findings.

## Historical presentation

**P. Hadjidoukas.** “Exploiting Task-Based Parallelism in Bayesian Uncertainty Quantification.” University of Patras, Department of Computer Engineering and Informatics, March 4, 2022. The uploaded `HPC_Applications.pdf` includes introductory programming examples, a runtime architecture slide, scientific applications, and a historical machine-learning task scheduling case study.

## Citation guidance

If your paper uses the **Torc-Lite runtime**, cite the PDP 2012 publication. Also cite additional application or algorithm papers where they are scientifically relevant. If you use **TorcPy**, cite the SoftwareX 2020 article separately. See the repository's `CITATION.cff` for the preferred machine-readable GitHub citation.
