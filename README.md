[![DOI](https://img.shields.io/badge/DOI-10.1137%2F22M1515665-blue)](https://doi.org/10.1137/22M1515665)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7414911.svg)](https://doi.org/10.5281/zenodo.7414911)


The repository contains the source code for the numerical experiments considered
in [Space Mapping for PDE Constrained Shape Optimization](https://doi.org/10.1137/22M1515665) by Sebastian Blauth.

To run the code, you have to install [cashocs](https://cashocs.readthedocs.io/)
first, which includes all necessary prerequisites. The results presented in this
repository have been obtained with version 2.0.0-alpha0 of cashocs (which uses FEniCS 2019.1).

The repository consists of the following test cases:

- A shape identification problem constrained by a semi-linear transmission problem (named `semi_linear_transmission_problem`) which is considered in Section 4.2 of the paper.

- A problem of uniform flow distribution constrained by the Navier-Stokes equations (named `uniform_flow_distribution`) which is considered in Section 4.3 of the paper.

In each of the directories, there is a `main.py` file, which can be used to run the code. 

Each problem is solved with the aggressive space mapping method for shape optimization presented in [Space Mapping for PDE Constrained Shape Optimization](https://doi.org/10.1137/22M1515665).

In the `visualization` directory, the file `visualization.py` generates the plots used in the paper. The repository is already initialized with the solutions obtained for the numerical examples in the paper, so that this can be run directly.

This software is citeable under the following DOI: [10.5281/zenodo.7414911](https://doi.org/10.5281/zenodo.7414911).

If you use the space mapping methods for your work, please cite the paper

	Space Mapping for PDE Constrained Shape Optimization
	Sebastian Blauth
	SIAM Journal on Optimization, Volume 33, Issue 3, 2023
	https://doi.org/10.1137/22M1515665

If you are using BibTeX, you can use the following entry:

	@Article{Blauth2023Space,
	  author   = {Blauth, Sebastian},
	  journal  = {SIAM J. Optim.},
	  title    = {Space {M}apping for {PDE} {C}onstrained {S}hape {O}ptimization},
	  year     = {2023},
	  issn     = {1052-6234,1095-7189},
	  number   = {3},
	  pages    = {1707--1733},
	  volume   = {33},
	  doi      = {10.1137/22M1515665},
	  fjournal = {SIAM Journal on Optimization},
	  mrclass  = {49Q10 (35Q93 49M41 65K05)},
	  mrnumber = {4622415},
	}
