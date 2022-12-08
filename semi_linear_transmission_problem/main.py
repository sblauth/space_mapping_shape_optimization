# Copyright (C) 2022 Sebastian Blauth

from fenics import *
import cashocs
import utils

sosm = cashocs.space_mapping.shape_optimization
cashocs.set_log_level(cashocs.LogLevel.ERROR)


cfg = cashocs.load_config("config.ini")
alpha_1 = 1.0
alpha_2 = 10.0
f_1 = 1.0
f_2 = 10.0
beta = 100.0

u_des_fixed = utils.create_desired_state(alpha_1, alpha_2, beta, f_1, f_2)

mesh, subdomains, boundaries, dx, ds, dS = cashocs.import_mesh("./mesh/mesh.xdmf")
V = FunctionSpace(mesh, "CG", 1)


u = Function(V)
p = Function(V)
u_des = Function(V)
F = (
    Constant(alpha_1) * dot(grad(u), grad(p)) * dx(1)
    + Constant(alpha_2) * dot(grad(u), grad(p)) * dx(2)
    - Constant(f_1) * p * dx(1)
    - Constant(f_2) * p * dx(2)
)
bcs = cashocs.create_dirichlet_bcs(V, Constant(0.0), boundaries, [1, 2, 3, 4])

J = cashocs.IntegralFunctional(Constant(0.5) * pow(u - u_des, 2) * dx)

coarse_model = sosm.CoarseModel(F, bcs, J, u, p, boundaries, config=cfg)
fine_model = utils.FineModel(mesh, alpha_1, alpha_2, beta, f_1, f_2, u_des_fixed)
u_fine = Function(V)


def hook():
    LagrangeInterpolator.interpolate(u_des, u_des_fixed)
    LagrangeInterpolator.interpolate(u_fine, fine_model.u)


u_param = Function(V)
J_param = cashocs.IntegralFunctional(Constant(0.5) * pow(u_param - u_fine, 2) * dx)

parameter_extraction = sosm.ParameterExtraction(
    coarse_model, J_param, u_param, config=cfg, mode="initial"
)

space_mapping = sosm.SpaceMapping(
    fine_model,
    coarse_model,
    parameter_extraction,
    method="broyden",
    max_iter=25,
    tol=1e-2,
    use_backtracking_line_search=False,
    broyden_type="good",
    memory_size=5,
    verbose=True,
    save_history=True,
)
space_mapping.inject_pre_callback(hook)
space_mapping.solve()
