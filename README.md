[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4432327.svg)](https://doi.org/10.5281/zenodo.4432327)




The repository contains the source code for the numerical experiments considered
in [Space Mapping for PDE Constrained Shape Optimization](https://arxiv.org) by Sebastian Blauth.

To run the code, you have to install [cashocs](https://cashocs.readthedocs.io/)
first, which includes all necessary prerequisites. The results presented in this
repository have been obtained with version 1.8.4 of cashocs (which uses FEniCS 2019.1).

The repository consists of the following test cases:

- A shape identification problem constrained by a semi-linear transmission problem (named `semi_linear_transmission_problem`) which is considered in Section 4.2 of the paper.

- A problem of uniform flow distribution constrained by the Navier-Stokes equations (named `uniform_flow_distribution`) which is considered in Section 4.3 of the paper.

In each of the directories, there is a `main.py` file, which can be used to run the code. 

Each problem is solved with the aggressive space mapping method for shape optimization presented in [Space Mapping for PDE Constrained Shape Optimization](https://arxiv.org).

In the `visualization` directory, the file `visualization.py` generates the plots used in the paper. The repository is already initialized with the solutions obtained for the numerical examples in the paper, so that this can be run directly.

This software is citeable under the following DOI: [10.5281/zenodo.4432327](https://doi.org/10.5281/zenodo.4432327).

If you use the space mapping for shape optimization in your work, please cite the following preprint:

    Nonlinear Conjugate Gradient Methods for PDE Constrained Shape Optimization Based on Steklov-Poincaré-Type Metrics
    Sebastian Blauth
    SIAM Journal on Optimization, Volume 31, Issue 3
    https://doi.org/10.1137/20M1367738

If you are using BibTeX, you can use the following entry:

    @Article{Blauth2020Nonlinear,
        author   = {Sebastian Blauth},
        journal  = {SIAM J. Optim.},
        title    = {{N}onlinear {C}onjugate {G}radient {M}ethods for {PDE} {C}onstrained {S}hape {O}ptimization {B}ased on {S}teklov-{P}oincaré-{T}ype {M}etrics},
        year     = {2021},
        number   = {3},
        pages    = {1658--1689},
        volume   = {31},
        doi      = {10.1137/20M1367738},
        fjournal = {SIAM Journal on Optimization},
    }
