"""
Created on 10/08/2022, 10.29

@author: blauths
"""

import cashocs
import fenics
import os

sosm = cashocs.space_mapping.shape_optimization

dir = os.path.dirname(os.path.realpath(__file__))


class FineModel(sosm.FineModel):
    def __init__(self, mesh, alpha_1, alpha_2, beta, f_1, f_2, u_des_fixed):
        super().__init__(mesh)
        self.u = fenics.Constant(0.0)
        self.iter = 0

        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.beta = beta
        self.f_1 = f_1
        self.f_2 = f_2
        self.u_des_fixed = u_des_fixed

    def solve_and_evaluate(self) -> None:
        self.iter += 1
        cashocs.io.write_out_mesh(
            self.mesh, "./mesh/mesh.msh", f"./mesh/fine/mesh_{self.iter}.msh"
        )
        cashocs.convert(
            f"{dir}/mesh/fine/mesh_{self.iter}.msh", f"{dir}/mesh/fine/mesh.xdmf"
        )
        mesh, subdomains, boundaries, dx, ds, dS = cashocs.import_mesh(
            "./mesh/fine/mesh.xdmf"
        )

        V = fenics.FunctionSpace(mesh, "CG", 1)
        u = fenics.Function(V)
        u_des = fenics.Function(V)
        v = fenics.TestFunction(V)
        F = (
            fenics.Constant(self.alpha_1)
            * fenics.dot(fenics.grad(u), fenics.grad(v))
            * dx(1)
            + fenics.Constant(self.alpha_2)
            * fenics.dot(fenics.grad(u), fenics.grad(v))
            * dx(2)
            + fenics.Constant(self.beta) * pow(u, 3) * v * dx
            - fenics.Constant(self.f_1) * v * dx(1)
            - fenics.Constant(self.f_2) * v * dx(2)
        )
        bcs = cashocs.create_dirichlet_bcs(
            V, fenics.Constant(0.0), boundaries, [1, 2, 3, 4]
        )
        cashocs.newton_solve(F, u, bcs, verbose=False)

        fenics.LagrangeInterpolator.interpolate(u_des, self.u_des_fixed)

        self.cost_functional_value = fenics.assemble(
            fenics.Constant(0.5) * pow(u - u_des, 2) * dx
        )
        self.u = u


def create_desired_state(alpha_1, alpha_2, beta, f_1, f_2):
    mesh, subdomains, boundaries, dx, ds, dS = cashocs.import_mesh(
        "./mesh/reference.xdmf"
    )
    V = fenics.FunctionSpace(mesh, "CG", 1)
    u = fenics.Function(V)
    v = fenics.TestFunction(V)
    F = (
        fenics.Constant(alpha_1) * fenics.dot(fenics.grad(u), fenics.grad(v)) * dx(1)
        + fenics.Constant(alpha_2) * fenics.dot(fenics.grad(u), fenics.grad(v)) * dx(2)
        + fenics.Constant(beta) * pow(u, 3) * v * dx
        - fenics.Constant(f_1) * v * dx(1)
        - fenics.Constant(f_2) * v * dx(2)
    )
    bcs = cashocs.create_dirichlet_bcs(
        V, fenics.Constant(0.0), boundaries, [1, 2, 3, 4]
    )
    cashocs.newton_solve(F, u, bcs, verbose=False)

    return u
