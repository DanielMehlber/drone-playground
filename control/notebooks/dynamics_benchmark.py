"""Batched flight-dynamics microbenchmarks for the dynamics notebook.

Compares NumPy / PyTorch nonlinear steps and current-state Jacobians
(analytic SymPy lambdify vs PyTorch autograd). Used by the evaluation
section in dynamics.ipynb.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import torch

# Open Robotics X3 defaults (see sim/worlds/quadcopter.sdf).
# k_t is motorConstant, N/(rad/s)^2. k_m is momentConstant, metres:
# shaft drag moment M = k_m * thrust. s matches Gazebo turningDirection
# (+1 CCW, -1 CW): rotors 0 and 1 CCW, rotors 2 and 3 CW.
X3 = {
    "m": 1.5,
    "g": 9.81,
    "dt": 1e-3,
    "I_xx": 0.0347563,
    "I_yy": 0.07,
    "I_zz": 0.0977,
    "k_t": 8.54858e-06,
    "k_m": 0.016,
    "s": np.array([1.0, 1.0, -1.0, -1.0], dtype=np.float64),
    "r": np.array(
        [
            [0.13, -0.22, 0.023],
            [-0.13, 0.20, 0.023],
            [0.13, 0.22, 0.023],
            [-0.13, -0.20, 0.023],
        ],
        dtype=np.float64,
    ),
}


def hover_thrust() -> float:
    """Thrust of one rotor at hover, mg/4, in newtons."""
    return float(X3["m"] * X3["g"] / 4.0)


def hover_speed() -> float:
    """Rotor speed (rad/s) whose thrust k_t * omega^2 equals the hover weight share."""
    return float(np.sqrt(hover_thrust() / X3["k_t"]))


def speeds_for_thrust(thrust: np.ndarray) -> np.ndarray:
    """Rotor speeds (rad/s) that produce the given thrusts through T = k_t * omega^2."""
    thrust = np.asarray(thrust, dtype=np.float64)
    return np.sqrt(np.maximum(thrust, 0.0) / float(X3["k_t"]))


def speed_sigma_for_thrust(thrust_sigma: float, speed: float | None = None) -> float:
    """Speed noise (rad/s) with the same dT as ``thrust_sigma`` newtons, at ``speed``."""
    if speed is None:
        speed = hover_speed()
    return float(thrust_sigma) / (2.0 * float(X3["k_t"]) * speed)


def _as_batch_state(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    return x.reshape(1, 13) if x.ndim == 1 else x


def _as_batch_input(u: np.ndarray, n: int) -> np.ndarray:
    u = np.asarray(u, dtype=np.float64)
    if u.ndim == 1:
        return np.repeat(u.reshape(1, 4), n, axis=0)
    return u


def quat_to_R_np(q: np.ndarray) -> np.ndarray:
    """SymPy Quaternion.to_rotation_matrix() for batch (N, 4)."""
    q0, q1, q2, q3 = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    n2 = q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3
    s = 2.0 / n2
    r00 = 1 - s * (q2 * q2 + q3 * q3)
    r01 = s * (q1 * q2 - q3 * q0)
    r02 = s * (q1 * q3 + q2 * q0)
    r10 = s * (q1 * q2 + q3 * q0)
    r11 = 1 - s * (q1 * q1 + q3 * q3)
    r12 = s * (q2 * q3 - q1 * q0)
    r20 = s * (q1 * q3 - q2 * q0)
    r21 = s * (q2 * q3 + q1 * q0)
    r22 = 1 - s * (q1 * q1 + q2 * q2)
    return np.stack(
        [
            np.stack([r00, r01, r02], axis=1),
            np.stack([r10, r11, r12], axis=1),
            np.stack([r20, r21, r22], axis=1),
        ],
        axis=1,
    )


def step_nonlinear_np(
    x: np.ndarray,
    u: np.ndarray,
    *,
    m: float = X3["m"],
    g: float = X3["g"],
    dt: float = X3["dt"],
    I_diag: np.ndarray | None = None,
    r: np.ndarray | None = None,
    k_t: float = X3["k_t"],
    k_m: float = X3["k_m"],
    spin: np.ndarray | None = None,
) -> np.ndarray:
    """Batched discrete map matching the notebook block equations (N,13).

    ``u`` is four rotor speeds in rad/s. Thrust is ``k_t * u^2`` along body +z.
    The shaft drag moment ``M = k_m * thrust`` enters body yaw as ``-spin * M``,
    with ``spin`` +1 CCW and -1 CW.
    """
    x = _as_batch_state(x)
    n = x.shape[0]
    u = _as_batch_input(u, n)
    if I_diag is None:
        I_diag = np.array([X3["I_xx"], X3["I_yy"], X3["I_zz"]], dtype=np.float64)
    if r is None:
        r = X3["r"]
    if spin is None:
        spin = X3["s"]
    I_inv = 1.0 / I_diag

    p = x[:, 0:3]
    v = x[:, 3:6]
    q = x[:, 6:10]
    w = x[:, 10:13]

    thrust = k_t * u * u
    F = np.zeros((n, 4, 3), dtype=np.float64)
    F[:, :, 2] = thrust
    tau = np.cross(r[None, :, :], F).sum(axis=1)
    tau[:, 2] -= k_m * (thrust * spin).sum(axis=1)

    Iw = I_diag * w
    gyro = np.cross(w, Iw)
    w_new = w + dt * (I_inv * (tau - gyro))

    omega_quat = np.concatenate([np.zeros((n, 1)), w], axis=1)
    q0, q1, q2, q3 = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    p0, p1, p2, p3 = omega_quat[:, 0], omega_quat[:, 1], omega_quat[:, 2], omega_quat[:, 3]
    q_omega = np.stack(
        [
            q0 * p0 - q1 * p1 - q2 * p2 - q3 * p3,
            q0 * p1 + q1 * p0 + q2 * p3 - q3 * p2,
            q0 * p2 - q1 * p3 + q2 * p0 + q3 * p1,
            q0 * p3 + q1 * p2 - q2 * p1 + q3 * p0,
        ],
        axis=1,
    )
    q_new = q + 0.5 * dt * q_omega

    R = quat_to_R_np(q)
    g_world = np.array([0.0, 0.0, -g], dtype=np.float64)
    # Notebook convention: world_to_body = R @ world_vec
    g_body = np.einsum("nij,j->ni", R, g_world)
    force = np.zeros((n, 3), dtype=np.float64)
    force[:, 2] = thrust.sum(axis=1)
    v_new = v + dt * (g_body + force / m)
    v_world = np.einsum("nji,nj->ni", R, v_new)
    p_new = p + dt * v_world

    return np.concatenate([p_new, v_new, q_new, w_new], axis=1)


def quat_to_R_torch(q: torch.Tensor) -> torch.Tensor:
    q0, q1, q2, q3 = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    n2 = q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3
    s = 2.0 / n2
    r00 = 1 - s * (q2 * q2 + q3 * q3)
    r01 = s * (q1 * q2 - q3 * q0)
    r02 = s * (q1 * q3 + q2 * q0)
    r10 = s * (q1 * q2 + q3 * q0)
    r11 = 1 - s * (q1 * q1 + q3 * q3)
    r12 = s * (q2 * q3 - q1 * q0)
    r20 = s * (q1 * q3 - q2 * q0)
    r21 = s * (q2 * q3 + q1 * q0)
    r22 = 1 - s * (q1 * q1 + q2 * q2)
    row0 = torch.stack([r00, r01, r02], dim=1)
    row1 = torch.stack([r10, r11, r12], dim=1)
    row2 = torch.stack([r20, r21, r22], dim=1)
    return torch.stack([row0, row1, row2], dim=1)


def step_nonlinear_torch(
    x: torch.Tensor,
    u: torch.Tensor,
    *,
    m: float = X3["m"],
    g: float = X3["g"],
    dt: float = X3["dt"],
    I_diag: torch.Tensor | None = None,
    r: torch.Tensor | None = None,
    k_t: float = X3["k_t"],
    k_m: float = X3["k_m"],
    spin: torch.Tensor | None = None,
) -> torch.Tensor:
    """Torch twin of ``step_nonlinear_np``. ``u`` is rotor speed in rad/s."""
    if x.ndim == 1:
        x = x.unsqueeze(0)
    if u.ndim == 1:
        u = u.unsqueeze(0).expand(x.shape[0], -1)
    n = x.shape[0]
    device, dtype = x.device, x.dtype
    if I_diag is None:
        I_diag = torch.tensor([X3["I_xx"], X3["I_yy"], X3["I_zz"]], device=device, dtype=dtype)
    if r is None:
        r = torch.tensor(X3["r"], device=device, dtype=dtype)
    if spin is None:
        spin = X3["s"]
    spin = torch.as_tensor(spin, device=device, dtype=dtype)
    I_inv = 1.0 / I_diag

    p, v, q, w = x[:, 0:3], x[:, 3:6], x[:, 6:10], x[:, 10:13]
    thrust = k_t * u * u
    F = torch.zeros(n, 4, 3, device=device, dtype=dtype)
    F[:, :, 2] = thrust
    tau = torch.cross(r.unsqueeze(0).expand(n, -1, -1), F, dim=2).sum(dim=1)
    tau[:, 2] = tau[:, 2] - k_m * (thrust * spin).sum(dim=1)

    Iw = I_diag * w
    gyro = torch.cross(w, Iw, dim=1)
    w_new = w + dt * (I_inv * (tau - gyro))

    zeros = torch.zeros(n, 1, device=device, dtype=dtype)
    omega_quat = torch.cat([zeros, w], dim=1)
    q0, q1, q2, q3 = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    p0, p1, p2, p3 = omega_quat[:, 0], omega_quat[:, 1], omega_quat[:, 2], omega_quat[:, 3]
    q_omega = torch.stack(
        [
            q0 * p0 - q1 * p1 - q2 * p2 - q3 * p3,
            q0 * p1 + q1 * p0 + q2 * p3 - q3 * p2,
            q0 * p2 - q1 * p3 + q2 * p0 + q3 * p1,
            q0 * p3 + q1 * p2 - q2 * p1 + q3 * p0,
        ],
        dim=1,
    )
    q_new = q + 0.5 * dt * q_omega

    R = quat_to_R_torch(q)
    g_world = torch.tensor([0.0, 0.0, -g], device=device, dtype=dtype)
    g_body = torch.einsum("nij,j->ni", R, g_world)
    force = torch.zeros(n, 3, device=device, dtype=dtype)
    force[:, 2] = thrust.sum(dim=1)
    v_new = v + dt * (g_body + force / m)
    v_world = torch.einsum("nji,nj->ni", R, v_new)
    p_new = p + dt * v_world
    return torch.cat([p_new, v_new, q_new, w_new], dim=1)


def jac_analytic_to_discrete(A: np.ndarray, B: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """Rate jacobians -> discrete ∂f/∂x, ∂f/∂u for x^{+} = x + dt * rate."""
    return np.eye(13) + dt * A, dt * B


def jac_autograd_torch(x: torch.Tensor, u: torch.Tensor, **kwargs: object) -> tuple[torch.Tensor, torch.Tensor]:
    """Discrete Jacobians ∂f/∂x, ∂f/∂u via autograd at one state."""
    x = x.detach().reshape(13)
    u = u.detach().reshape(4)

    def f_x(z: torch.Tensor) -> torch.Tensor:
        return step_nonlinear_torch(z, u, **kwargs).reshape(13)

    def f_u(w: torch.Tensor) -> torch.Tensor:
        return step_nonlinear_torch(x, w, **kwargs).reshape(13)

    return (
        torch.autograd.functional.jacobian(f_x, x),
        torch.autograd.functional.jacobian(f_u, u),
    )


@dataclass
class BenchResult:
    name: str
    batch_size: int
    steps: int
    seconds: float
    steps_per_sec: float
    us_per_step_item: float


def _time_call(fn: Callable[[], None], warmup: int = 2) -> float:
    for _ in range(warmup):
        fn()
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def random_batch(
    n: int,
    *,
    rng: np.random.Generator,
    hover: float | None = None,
    speed_sigma: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """States near hover and rotor speeds near the hover speed.

    The default speed noise has the same thrust derivative as 0.05 N.
    """
    if hover is None:
        hover = hover_speed()
    if speed_sigma is None:
        speed_sigma = speed_sigma_for_thrust(0.05, hover)
    x = np.zeros((n, 13), dtype=np.float64)
    x[:, 6] = 1.0
    x[:, 0:3] = rng.normal(0.0, 0.05, size=(n, 3))
    x[:, 3:6] = rng.normal(0.0, 0.1, size=(n, 3))
    x[:, 7:10] = rng.normal(0.0, 0.02, size=(n, 3))
    q = x[:, 6:10]
    x[:, 6:10] = q / np.linalg.norm(q, axis=1, keepdims=True)
    x[:, 10:13] = rng.normal(0.0, 0.2, size=(n, 3))
    u = hover + rng.normal(0.0, speed_sigma, size=(n, 4))
    return x, u


def run_timing_suite(
    jac_analytic_np: Callable[[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]],
    batch_sizes: list[int],
    steps: int = 100,
    seed: int = 0,
) -> list[BenchResult]:
    rng = np.random.default_rng(seed)
    results: list[BenchResult] = []
    device = torch.device("cpu")
    dt = float(X3["dt"])

    for n in batch_sizes:
        x_np, u_np = random_batch(n, rng=rng)
        x_t = torch.tensor(x_np, dtype=torch.float64, device=device)
        u_t = torch.tensor(u_np, dtype=torch.float64, device=device)

        # Precompute analytic discrete maps once per item (EKF-style reuse within the window).
        Ad = np.empty((n, 13, 13), dtype=np.float64)
        Bd = np.empty((n, 13, 4), dtype=np.float64)
        for i in range(n):
            A, B = jac_analytic_np(x_np[i], u_np[i])
            Ad[i], Bd[i] = jac_analytic_to_discrete(A, B, dt)
        Ad_t = torch.tensor(Ad, dtype=torch.float64, device=device)
        Bd_t = torch.tensor(Bd, dtype=torch.float64, device=device)
        dx = np.zeros_like(x_np)
        du = np.zeros_like(u_np)
        dx_t = torch.zeros_like(x_t)
        du_t = torch.zeros_like(u_t)

        # Jacobian paths are O(N) Python calls; keep wall time bounded at large N.
        jac_steps = steps if n <= 16 else max(5, min(20, steps // max(1, n // 8)))

        variants: list[tuple[str, Callable[[], None], int]] = []

        def make_np_nl(steps_: int = steps) -> Callable[[], None]:
            def _run() -> None:
                x = x_np
                for _ in range(steps_):
                    x = step_nonlinear_np(x, u_np)

            return _run

        def make_torch_nl(steps_: int = steps) -> Callable[[], None]:
            def _run() -> None:
                x = x_t
                for _ in range(steps_):
                    x = step_nonlinear_torch(x, u_t)

            return _run

        def make_np_linear(steps_: int = steps) -> Callable[[], None]:
            def _run() -> None:
                d = dx
                for _ in range(steps_):
                    # Batched: d^{+} = Ad d + Bd du  (einsum over batch).
                    d = np.einsum("nij,nj->ni", Ad, d) + np.einsum("nij,nj->ni", Bd, du)

            return _run

        def make_torch_linear(steps_: int = steps) -> Callable[[], None]:
            def _run() -> None:
                d = dx_t
                for _ in range(steps_):
                    d = torch.bmm(Ad_t, d.unsqueeze(-1)).squeeze(-1) + torch.bmm(Bd_t, du_t.unsqueeze(-1)).squeeze(-1)

            return _run

        def make_np_jac(steps_: int = jac_steps) -> Callable[[], None]:
            def _run() -> None:
                for _ in range(steps_):
                    for i in range(n):
                        jac_analytic_np(x_np[i], u_np[i])

            return _run

        def make_torch_jac_analytic(steps_: int = jac_steps) -> Callable[[], None]:
            def _run() -> None:
                for _ in range(steps_):
                    for i in range(n):
                        A, B = jac_analytic_np(x_np[i], u_np[i])
                        _ = torch.as_tensor(A, dtype=torch.float64, device=device)
                        _ = torch.as_tensor(B, dtype=torch.float64, device=device)

            return _run

        def make_torch_jac_autograd(steps_: int = jac_steps) -> Callable[[], None]:
            def _run() -> None:
                for _ in range(steps_):
                    for i in range(n):
                        jac_autograd_torch(x_t[i], u_t[i])

            return _run

        variants = [
            ("numpy_nonlinear", make_np_nl(), n * steps),
            ("torch_nonlinear", make_torch_nl(), n * steps),
            ("numpy_linear_map", make_np_linear(), n * steps),
            ("torch_linear_map", make_torch_linear(), n * steps),
            ("numpy_jacobian_analytic", make_np_jac(), n * jac_steps),
            ("torch_jacobian_analytic", make_torch_jac_analytic(), n * jac_steps),
            ("torch_jacobian_autograd", make_torch_jac_autograd(), n * jac_steps),
        ]

        for name, fn, work in variants:
            sec = _time_call(fn)
            results.append(
                BenchResult(
                    name=name,
                    batch_size=n,
                    steps=work // n,
                    seconds=sec,
                    steps_per_sec=work / sec if sec > 0 else float("inf"),
                    us_per_step_item=1e6 * sec / work if work else float("inf"),
                )
            )
    return results


def measure_errors(
    jac_analytic_np: Callable[[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]],
    *,
    n_samples: int = 48,
    seed: int = 1,
    delta_scale: float = 1e-4,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    x, u = random_batch(n_samples, rng=rng)
    dt = float(X3["dt"])

    jac_diffs: list[float] = []
    lin_errs: list[float] = []
    nl_torch_errs: list[float] = []

    for i in range(n_samples):
        A, B = jac_analytic_np(x[i], u[i])
        Ad, Bd = jac_analytic_to_discrete(A, B, dt)

        xt = torch.tensor(x[i], dtype=torch.float64)
        ut = torch.tensor(u[i], dtype=torch.float64)
        Jx, Ju = jac_autograd_torch(xt, ut)
        jac_diffs.append(
            float(
                max(
                    np.linalg.norm(Ad - Jx.detach().numpy()),
                    np.linalg.norm(Bd - Ju.detach().numpy()),
                )
            )
        )

        dx = rng.normal(0.0, delta_scale, size=13)
        q = x[i, 6:10]
        dx[6:10] -= q * np.dot(q, dx[6:10])
        du = rng.normal(0.0, delta_scale, size=4)

        x2 = x[i] + dx
        x2[6:10] /= np.linalg.norm(x2[6:10])
        u2 = u[i] + du
        f1 = step_nonlinear_np(x[i], u[i])[0]
        f2 = step_nonlinear_np(x2, u2)[0]
        f_lin = f1 + Ad @ dx + Bd @ du
        lin_errs.append(float(np.linalg.norm(f2 - f_lin)))

        f_torch = step_nonlinear_torch(xt, ut).detach().numpy().reshape(13)
        nl_torch_errs.append(float(np.linalg.norm(f1 - f_torch)))

    return {
        "jac_analytic_vs_autograd_max": float(np.max(jac_diffs)),
        "jac_analytic_vs_autograd_mean": float(np.mean(jac_diffs)),
        "linear_onestep_err_mean": float(np.mean(lin_errs)),
        "linear_onestep_err_max": float(np.max(lin_errs)),
        "numpy_vs_torch_nonlinear_max": float(np.max(nl_torch_errs)),
        "delta_scale": delta_scale,
        "n_samples": float(n_samples),
    }


def results_to_arrays(
    results: list[BenchResult],
) -> dict[str, dict[str, np.ndarray]]:
    """name -> {batch_sizes, us_per_step_item, steps_per_sec}."""
    names = sorted({r.name for r in results})
    out: dict[str, dict[str, np.ndarray]] = {}
    for name in names:
        rows = sorted([r for r in results if r.name == name], key=lambda r: r.batch_size)
        out[name] = {
            "batch_sizes": np.array([r.batch_size for r in rows]),
            "us_per_step_item": np.array([r.us_per_step_item for r in rows]),
            "steps_per_sec": np.array([r.steps_per_sec for r in rows]),
            "seconds": np.array([r.seconds for r in rows]),
        }
    return out
