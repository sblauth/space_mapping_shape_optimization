[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6979620.svg)](https://doi.org/10.5281/zenodo.6979620)



The repository contains the source code for the numerical experiments considered
in [Space Mapping for PDE Constrained Shape Optimization](https://github.com/sblauth/space_mapping_shape_optimization) by Sebastian Blauth.

To run the code, you have to install [cashocs](https://cashocs.readthedocs.io/)
first, which includes all necessary prerequisites. The results presented in this
repository have been obtained with version 1.8.4 of cashocs (which uses FEniCS 2019.1).

The repository consists of the following test cases:

- A shape identification problem constrained by a semi-linear transmission problem (named `semi_linear_transmission_problem`) which is considered in Section 4.2 of the paper.

- A problem of uniform flow distribution constrained by the Navier-Stokes equations (named `uniform_flow_distribution`) which is considered in Section 4.3 of the paper.

In each of the directories, there is a `main.py` file, which can be used to run the code. 

Each problem is solved with the aggressive space mapping method for shape optimization presented in [Space Mapping for PDE Constrained Shape Optimization](https://github.com/sblauth/space_mapping_shape_optimization).

In the `visualization` directory, the file `visualization.py` generates the plots used in the paper. The repository is already initialized with the solutions obtained for the numerical examples in the paper, so that this can be run directly.

This software is citeable under the following DOI: [10.5281/zenodo.6979620](https://doi.org/10.5281/zenodo.6979620).

