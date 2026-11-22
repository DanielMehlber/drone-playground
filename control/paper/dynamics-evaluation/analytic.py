"""Analytic current-state rate Jacobians for the evaluation study.

Same discrete block map as ``control/notebooks/dynamics.ipynb``. The symbolic
13 x 13 matrix is not printed. ``build_jacobians`` returns NumPy callables.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from sympy import Matrix, Quaternion, lambdify, symbols

NOTEBOOKS = Path(__file__).resolve().parents[2] / "notebooks"
sys.path.insert(0, str(NOTEBOOKS))

from dynamics_benchmark import X3  # noqa: E402


def build_jacobians() -> tuple[object, object]:
    """Return ``(rate_jacobians, nonlinear_f)`` NumPy callables.

    ``rate_jacobians(x, u, dt) -> (A, B)`` with ``A`` shape (13, 13) and ``B``
    shape (13, 4). ``nonlinear_f(x, u, dt) -> (13,)`` is the symbolic map,
    used only to check the block step.
    """
    mass, gravity, step = symbols("m g dt", real=True)
    inertia_xx, inertia_yy, inertia_zz = symbols("I_xx I_yy I_zz", real=True, positive=True)
    inertia = Matrix.diag(inertia_xx, inertia_yy, inertia_zz)
    inertia_inv = Matrix.diag(1 / inertia_xx, 1 / inertia_yy, 1 / inertia_zz)
    world_gravity = Matrix([0, 0, -gravity])

    rotor_symbols = []
    rotors = []
    for index in range(1, 5):
        components = symbols(f"r{index}x r{index}y r{index}z", real=True)
        rotor_symbols.extend(components)
        rotors.append(Matrix(components))

    thrust_symbols = symbols("f1 f2 f3 f4", real=True)
    forces = [Matrix([0, 0, thrust]) for thrust in thrust_symbols]

    px, py, pz = symbols("x y z", real=True)
    vx, vy, vz = symbols("v_x v_y v_z", real=True)
    q0, q1, q2, q3 = symbols("q0 q1 q2 q3", real=True)
    wx, wy, wz = symbols("w_x w_y w_z", real=True)
    attitude = Quaternion(q0, q1, q2, q3)
    position = Matrix([px, py, pz])
    velocity = Matrix([vx, vy, vz])
    rates = Matrix([wx, wy, wz])
    state = Matrix([position, velocity, attitude.to_Matrix(), rates])

    rotation = attitude.to_rotation_matrix()
    torque = sum((rotor.cross(force) for rotor, force in zip(rotors, forces, strict=True)), Matrix.zeros(3, 1))
    momentum = inertia * rates
    gyroscopic = rates.cross(momentum)
    angular_acceleration = inertia_inv * (torque - gyroscopic)
    new_rates = rates + angular_acceleration * step
    omega_quat = Quaternion(0, rates[0], rates[1], rates[2])
    new_attitude = attitude + attitude * omega_quat * step / 2

    body_gravity = rotation * world_gravity
    body_thrust = sum(forces, Matrix.zeros(3, 1))
    new_velocity = velocity + (body_gravity + body_thrust / mass) * step
    new_position = position + (rotation.T * new_velocity) * step
    new_state = Matrix([new_position, new_velocity, new_attitude.to_Matrix(), new_rates])

    rate = (new_state - state) / step
    state_jacobian = rate.jacobian(state)
    input_jacobian = rate.jacobian(Matrix(thrust_symbols))

    arguments = (
        px,
        py,
        pz,
        vx,
        vy,
        vz,
        q0,
        q1,
        q2,
        q3,
        wx,
        wy,
        wz,
        *thrust_symbols,
        mass,
        gravity,
        step,
        inertia_xx,
        inertia_yy,
        inertia_zz,
        *rotor_symbols,
    )
    constants = (
        float(X3["m"]),
        float(X3["g"]),
        float(X3["I_xx"]),
        float(X3["I_yy"]),
        float(X3["I_zz"]),
        *X3["r"].reshape(-1).tolist(),
    )
    jac_fn = lambdify(arguments, (state_jacobian, input_jacobian), modules="numpy", cse=True, docstring_limit=0)
    f_fn = lambdify(arguments, new_state, modules="numpy", cse=True, docstring_limit=0)

    def _eval(fn: object, state_vec: np.ndarray, control: np.ndarray, dt: float) -> object:
        state_vals = np.asarray(state_vec, dtype=float).reshape(13)
        control_vals = np.asarray(control, dtype=float).reshape(4)
        return fn(  # type: ignore[operator]
            *state_vals,
            *control_vals,
            constants[0],
            constants[1],
            float(dt),
            *constants[2:],
        )

    def rate_jacobians(state_vec: np.ndarray, control: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
        raw_a, raw_b = _eval(jac_fn, state_vec, control, dt)
        return (
            np.asarray(raw_a, dtype=np.float64).reshape(13, 13),
            np.asarray(raw_b, dtype=np.float64).reshape(13, 4),
        )

    def nonlinear_map(state_vec: np.ndarray, control: np.ndarray, dt: float) -> np.ndarray:
        raw = _eval(f_fn, state_vec, control, dt)
        return np.asarray(raw, dtype=np.float64).reshape(13)

    return rate_jacobians, nonlinear_map
