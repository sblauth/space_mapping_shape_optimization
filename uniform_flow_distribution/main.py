# Copyright (C) 2022 Sebastian Blauth

from fenics import *
import cashocs
import os
import json
import utils


dir = os.path.dirname(os.path.realpath(__file__))
sosm = cashocs.space_mapping.shape_optimization
cashocs.set_log_level(cashocs.LogLevel.ERROR)

cfg = cashocs.load_config("./config.ini")
cfg.set("Output", "verbose", "False")

Re = 100.0

mesh, subdomains, boundaries, dx, ds, dS = cashocs.import_mesh("./mesh/mesh.xdmf")
n = FacetNormal(mesh)

u_in = Expression(("6.0*(0.0 - x[1])*(x[1] + 1.0)", "0.0"), degree=2)
q_in = -assemble(dot(u_in, n) * ds(1))
output_list = []

v_elem = VectorElement("CG", mesh.ufl_cell(), 2)
p_elem = FiniteElement("CG", mesh.ufl_cell(), 1)
V = FunctionSpace(mesh, v_elem * p_elem)

up = Function(V)

u, p = split(up)
vq = Function(V)
v, q = split(vq)

F = inner(grad(u), grad(v)) * dx - p * div(v) * dx - q * div(u) * dx

bc_in = DirichletBC(V.sub(0), u_in, boundaries, 1)
bcs_wall = cashocs.create_dirichlet_bcs(
    V.sub(0), Constant((0.0, 0.0)), boundaries, [2, 3, 4]
)
bc_out = DirichletBC(V.sub(0).sub(0), Constant(0.0), boundaries, 5)
bc_pressure = DirichletBC(V.sub(1), Constant(0.0), boundaries, 5)
bcs = [bc_in] + bcs_wall + [bc_out] + [bc_pressure]

J = [cashocs.ScalarTrackingFunctional(dot(u, n) * ds(i), q_in / 3) for i in range(5, 8)]

coarse_model = sosm.CoarseModel(F, bcs, J, up, vq, boundaries, config=cfg)
fine_model = utils.FineModel(mesh, Re, q_in, output_list)

up_param = Function(V)
u_param, p_param = split(up_param)
J_param = Constant(0.0) * dx
J_param_tracking = fine_model.J_tracking
for idx, i in enumerate(range(5, 8)):
    J_param_tracking[idx]["integrand"] = dot(u_param, n) * ds(i)

parameter_extraction = sosm.ParameterExtraction(
    coarse_model, J_param, up_param, config=cfg, scalar_tracking_forms=J_param_tracking
)

space_mapping = sosm.SpaceMapping(
    fine_model,
    coarse_model,
    parameter_extraction,
    method="broyden",
    max_iter=25,
    tol=1e-4,
    use_backtracking_line_search=False,
    broyden_type="good",
    memory_size=5,
)

space_mapping.solve()

with open("./flow_values.json", "w") as file:
    json.dump(output_list, file)
