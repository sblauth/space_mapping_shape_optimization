# Copyright (C) 2022 Sebastian Blauth

import ctypes

import cashocs
import fenics
import os
import subprocess

sosm = cashocs.space_mapping.shape_optimization

dir = os.path.dirname(os.path.realpath(__file__))


class FineModel(sosm.FineModel):
    def __init__(self, mesh, Re, q_in, output_list):
        super().__init__(mesh)

        self.tracking_goals = [ctypes.c_double(0.0) for _ in range(5, 8)]
        self.iter = 0

        self.Re = Re
        self.q_in = q_in
        self.output_list = output_list

    def solve_and_evaluate(self):
        self.iter += 1

        # write out the mesh
        cashocs.io.write_out_mesh(
            self.mesh, "./mesh/mesh.msh", f"./mesh/fine/mesh_{self.iter}.msh"
        )
        cashocs.io.write_out_mesh(self.mesh, "./mesh/mesh.msh", f"./mesh/fine/mesh.msh")

        subprocess.run(
            ["gmsh", "./mesh/fine.geo", "-2", "-o", "./mesh/fine/fine.msh"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cashocs.convert("./mesh/fine/fine.msh", "./mesh/fine/fine.xdmf")

        mesh, subdomains, boundaries, dx, ds, dS = cashocs.import_mesh(
            "./mesh/fine/fine.xdmf"
        )
        n = fenics.FacetNormal(mesh)
        v_elem = fenics.VectorElement("CG", mesh.ufl_cell(), 2)
        p_elem = fenics.FiniteElement("CG", mesh.ufl_cell(), 1)
        V = fenics.FunctionSpace(mesh, v_elem * p_elem)
        R = fenics.FunctionSpace(mesh, "R", 0)

        up = fenics.Function(V)
        u, p = fenics.split(up)
        v, q = fenics.TestFunctions(V)

        F = (
            fenics.inner(fenics.grad(u), fenics.grad(v)) * dx
            + fenics.Constant(self.Re) * fenics.inner(fenics.grad(u) * u, v) * dx
            - p * fenics.div(v) * dx
            - q * fenics.div(u) * dx
        )

        u_in = fenics.Expression(("6.0*(0.0 - x[1])*(x[1] + 1.0)", "0.0"), degree=2)
        bc_in = fenics.DirichletBC(V.sub(0), u_in, boundaries, 1)
        bcs_wall = cashocs.create_dirichlet_bcs(
            V.sub(0), fenics.Constant((0.0, 0.0)), boundaries, [2, 3, 4]
        )
        bc_out = fenics.DirichletBC(
            V.sub(0).sub(0), fenics.Constant(0.0), boundaries, 5
        )
        bc_pressure = fenics.DirichletBC(V.sub(1), fenics.Constant(0.0), boundaries, 5)
        bcs = [bc_in] + bcs_wall + [bc_out] + [bc_pressure]

        cashocs.newton_solve(F, up, bcs, verbose=False)
        u, p = up.split(True)

        file = fenics.File(f"./pvd/u_{self.iter}.pvd")
        file.write(u)

        J_list = [
            cashocs.ScalarTrackingFunctional(fenics.dot(u, n) * ds(i), self.q_in / 3)
            for i in range(5, 8)
        ]
        self.cost_functional_value = cashocs._utils.summation(
            [J.evaluate() for J in J_list]
        )

        self.flow_values = [
            fenics.assemble(fenics.dot(u, n) * ds(i)) for i in range(5, 8)
        ]
        self.output_list.append(self.flow_values)

        for idx in range(len(self.tracking_goals)):
            self.tracking_goals[idx].value = self.flow_values[idx]
