"""Scenario rollouts, trajectory error, and batch timings for the paper.

Run from this directory: ``python study.py``.

The error baseline is the nonlinear NumPy step at 0.1 ms. A coarser nonlinear
step uses that same map with a larger ``dt``. The linear trajectory freezes
the analytic Jacobian at the state at the start of each coarse interval and
applies the affine map at the 0.1 ms reference step until the interval ends.
GPU placements are timed only when ``torch.cuda.is_available()`` is true.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path


def _prefer_matching_mpl_toolkits() -> None:
    """Drop a distro mpl_toolkits that is older than the installed Matplotlib.

    That copy imports ``matplotlib.tri.triangulation``, which Matplotlib 3.11
    no longer provides, and then 3D axes fail to register.
    """
    kept: list[str] = []
    for entry in sys.path:
        axes = Path(entry) / "mpl_toolkits" / "mplot3d" / "axes3d.py"
        if axes.is_file() and "matplotlib.tri.triangulation" in axes.read_text(errors="ignore"):
            continue
        kept.append(entry)
    sys.path[:] = kept
    # A distro .pth file loads the old package before this script runs.
    for name in list(sys.modules):
        if name == "mpl_toolkits" or name.startswith("mpl_toolkits."):
            del sys.modules[name]


_prefer_matching_mpl_toolkits()

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np
import torch

HERE = Path(__file__).resolve().parent
NOTEBOOKS = HERE.parents[1] / "notebooks"
sys.path.insert(0, str(NOTEBOOKS))

from analytic import build_jacobians  # noqa: E402

from dynamics_benchmark import (  # noqa: E402
    X3,
    jac_analytic_to_discrete,
    jac_autograd_torch,
    quat_to_R_np,
    step_nonlinear_np,
    step_nonlinear_torch,
)

FIG = HERE / "figures"
GENERATED = HERE / "generated"
DT_REF = 1e-4
HORIZON = 2.0
COARSE_DTS = (5e-4, 1e-3, 2e-3, 5e-3, 1e-2)
BATCH_SIZES = (1, 8, 32, 128, 512, 2048)
SCENARIOS = ("hover", "pitch_pulse", "roll_reversal", "climb_pitch")
SCENARIO_LABELS = {
    "hover": "Hover",
    "pitch_pulse": "Pitch pulse",
    "roll_reversal": "Roll reversal",
    "climb_pitch": "Climb with pitch",
}


def hover_thrust() -> float:
    return float(X3["m"] * X3["g"] / 4.0)


def initial_state() -> np.ndarray:
    state = np.zeros(13, dtype=np.float64)
    state[2] = 1.0
    state[6] = 1.0
    return state


def normalize_state(state: np.ndarray) -> np.ndarray:
    out = np.array(state, dtype=np.float64, copy=True)
    quat = out[6:10]
    out[6:10] = quat / np.linalg.norm(quat)
    return out


def schedule(kind: str, time_s: float) -> np.ndarray:
    """Open-loop rotor forces (N). Zero-order hold on whatever grid calls this."""
    base = hover_thrust()
    control = np.full(4, base)
    front = (0, 2)
    rear = (1, 3)
    left = (1, 2)
    right = (0, 3)
    if kind == "hover":
        return control
    if kind == "pitch_pulse":
        if time_s < 0.4:
            bias = 0.35
        elif time_s < 0.8:
            bias = -0.35
        else:
            return control
        control[list(front)] += bias
        control[list(rear)] -= bias
        return np.maximum(control, 0.0)
    if kind == "roll_reversal":
        if time_s < 0.4:
            bias = 0.12
        elif time_s < 0.8:
            bias = -0.12
        else:
            return control
        control[list(left)] += bias
        control[list(right)] -= bias
        return np.maximum(control, 0.0)
    if kind == "climb_pitch":
        # Collective above hover, plus a small sustained nose-down bias.
        # The bias is a few hundredths of a newton so the open-loop pitch
        # stays well short of a flip over the two-second horizon.
        control[:] = base * 1.08
        control[list(front)] += 0.02
        control[list(rear)] -= 0.02
        return control
    raise KeyError(kind)


def controls_on_grid(kind: str, dt: float, horizon: float = HORIZON) -> np.ndarray:
    count = round(horizon / dt)
    times = dt * np.arange(count)
    return np.stack([schedule(kind, float(stamp)) for stamp in times], axis=0)


def step_one(state: np.ndarray, control: np.ndarray, dt: float) -> np.ndarray:
    return step_nonlinear_np(state, control, dt=dt)[0]


def rollout_nonlinear(kind: str, dt: float) -> tuple[np.ndarray, np.ndarray]:
    controls = controls_on_grid(kind, dt)
    state = initial_state()
    states = [state]
    for control in controls:
        state = normalize_state(step_one(state, control, dt))
        states.append(state)
    times = dt * np.arange(len(states))
    return times, np.stack(states)


def rollout_linear_held(
    kind: str,
    dt: float,
    rate_jacobians: Callable[[np.ndarray, np.ndarray, float], tuple[np.ndarray, np.ndarray]],
) -> tuple[np.ndarray, np.ndarray]:
    """Freeze A, B at the start of each coarse interval; affine-map at dt_ref inside it."""
    if abs(dt / DT_REF - round(dt / DT_REF)) > 1e-8:
        raise ValueError(f"{dt} is not a multiple of the reference step")
    substeps = round(dt / DT_REF)
    controls = controls_on_grid(kind, dt)
    state = initial_state()
    states = [state]
    for control in controls:
        state_jacobian, input_jacobian = rate_jacobians(state, control, DT_REF)
        discrete_a, discrete_b = jac_analytic_to_discrete(state_jacobian, input_jacobian, DT_REF)
        anchor = state
        predicted = step_one(anchor, control, DT_REF)
        delta_u = np.zeros(4, dtype=np.float64)
        for _ in range(substeps):
            deviation = state - anchor
            state = predicted + discrete_a @ deviation + discrete_b @ delta_u
        state = normalize_state(state)
        states.append(state)
    times = dt * np.arange(len(states))
    return times, np.stack(states)


def geodesic_angle(q_est: np.ndarray, q_ref: np.ndarray) -> np.ndarray:
    """Quaternion geodesic (rad) for shapes (..., 4)."""
    dots = np.abs(np.sum(q_est * q_ref, axis=-1))
    return 2.0 * np.arccos(np.clip(dots, 0.0, 1.0))


def trajectory_errors(estimate: np.ndarray, reference: np.ndarray, dt: float) -> dict[str, float]:
    """Compare a coarse rollout to the fine reference at the coarse knots."""
    if estimate.shape[0] != round(HORIZON / dt) + 1:
        raise ValueError("coarse trajectory length does not match the horizon")
    stride = round(dt / DT_REF)
    ref = reference[::stride]
    if ref.shape[0] != estimate.shape[0]:
        raise ValueError("reference subsampling does not land on coarse knots")
    pos = np.linalg.norm(estimate[:, 0:3] - ref[:, 0:3], axis=1)
    ang = geodesic_angle(estimate[:, 6:10], ref[:, 6:10])
    # Drop the shared initial state so the mean is the error accumulated in the run.
    pos_body = pos[1:]
    ang_body = ang[1:]
    return {
        "pos_rmse_m": float(np.sqrt(np.mean(pos_body**2))),
        "pos_horizon_m": float(pos[-1]),
        "att_rmse_deg": float(np.degrees(np.sqrt(np.mean(ang_body**2)))),
        "att_horizon_deg": float(np.degrees(ang[-1])),
    }


def body_z_world(quaternions: np.ndarray) -> np.ndarray:
    rotation = quat_to_R_np(quaternions)
    return rotation[:, 2, :]


def tilt_deg(quaternions: np.ndarray) -> np.ndarray:
    vertical = np.clip(body_z_world(quaternions)[:, 2], -1.0, 1.0)
    return np.degrees(np.arccos(vertical))


def cpu_model() -> str:
    for line in Path("/proc/cpuinfo").read_text().splitlines():
        if line.startswith("model name"):
            return line.split(":", 1)[1].strip()
    return platform.processor() or platform.machine()


def memory_gib() -> float:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemTotal:"):
            kib = float(line.split()[1])
            return kib / (1024.0**2)
    return float("nan")


def nvidia_smi_text() -> str:
    try:
        completed = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {type(exc).__name__}"
    text = (completed.stdout or completed.stderr).strip()
    if completed.returncode != 0:
        return f"exit {completed.returncode}: {text}"
    return text or "no device lines"


def hardware_record() -> dict[str, object]:
    cuda = bool(torch.cuda.is_available())
    gpu: dict[str, object] = {
        "cuda_available": cuda,
        "nvidia_smi": nvidia_smi_text(),
        "torch_cuda_version": torch.version.cuda,
        "device_name": None,
        "total_memory_bytes": None,
    }
    if cuda:
        props = torch.cuda.get_device_properties(0)
        gpu["device_name"] = torch.cuda.get_device_name(0)
        gpu["total_memory_bytes"] = int(props.total_memory)
        gpu["capability"] = f"{props.major}.{props.minor}"
    return {
        "platform": platform.platform(),
        "cpu_model": cpu_model(),
        "cpu_count": platform.os.cpu_count(),
        "memory_gib": memory_gib(),
        "torch": torch.__version__,
        "numpy": np.__version__,
        "gpu": gpu,
    }


def _time_call(fn: Callable[[], None], *, warmup: int, repeats: int = 1) -> float:
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - t0)
    return float(min(samples))


def _sync_if_cuda(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def jacobian_work(batch: int) -> tuple[int, int]:
    """Inner steps and warmups for analytic Jacobian vs autograd."""
    if batch <= 8:
        return 8, 2
    if batch <= 32:
        return 4, 1
    if batch <= 128:
        return 2, 1
    return 1, 1


def propagation_steps(batch: int) -> int:
    if batch <= 128:
        return 40
    if batch <= 512:
        return 20
    return 10


def speed_records(
    rate_jacobians: Callable[[np.ndarray, np.ndarray, float], tuple[np.ndarray, np.ndarray]],
) -> list[dict[str, object]]:
    rng = np.random.default_rng(0)
    dt = float(X3["dt"])
    records: list[dict[str, object]] = []
    cuda = bool(torch.cuda.is_available())
    devices = [torch.device("cpu")]
    if cuda:
        devices.append(torch.device("cuda"))

    def add(name: str, batch: int, steps: int, seconds: float, placement: str) -> None:
        work = batch * steps
        records.append(
            {
                "name": name,
                "batch_size": batch,
                "steps": steps,
                "seconds": seconds,
                "us_per_step_item": 1e6 * seconds / work,
                "items_per_s": work / seconds,
                "placement": placement,
            }
        )

    for batch in BATCH_SIZES:
        hover = hover_thrust()
        state_np = np.zeros((batch, 13), dtype=np.float64)
        state_np[:, 6] = 1.0
        state_np[:, 0:3] = rng.normal(0.0, 0.05, size=(batch, 3))
        state_np[:, 3:6] = rng.normal(0.0, 0.05, size=(batch, 3))
        state_np[:, 7:10] = rng.normal(0.0, 0.01, size=(batch, 3))
        quat = state_np[:, 6:10]
        state_np[:, 6:10] = quat / np.linalg.norm(quat, axis=1, keepdims=True)
        state_np[:, 10:13] = rng.normal(0.0, 0.05, size=(batch, 3))
        control_np = hover + rng.normal(0.0, 0.02, size=(batch, 4))

        steps = propagation_steps(batch)
        jac_steps, jac_warmup = jacobian_work(batch)

        def run_numpy_nonlinear(
            state_np: np.ndarray = state_np,
            control_np: np.ndarray = control_np,
            steps: int = steps,
        ) -> None:
            state = state_np
            for _ in range(steps):
                state = step_nonlinear_np(state, control_np)

        discrete_a = np.empty((batch, 13, 13), dtype=np.float64)
        discrete_b = np.empty((batch, 13, 4), dtype=np.float64)
        for index in range(batch):
            state_jacobian, input_jacobian = rate_jacobians(state_np[index], control_np[index], dt)
            discrete_a[index], discrete_b[index] = jac_analytic_to_discrete(state_jacobian, input_jacobian, dt)
        deviation = np.zeros_like(state_np)
        delta_u = np.zeros_like(control_np)

        def run_numpy_linear(
            deviation: np.ndarray = deviation,
            delta_u: np.ndarray = delta_u,
            discrete_a: np.ndarray = discrete_a,
            discrete_b: np.ndarray = discrete_b,
            steps: int = steps,
        ) -> None:
            state = deviation
            for _ in range(steps):
                state = np.einsum("nij,nj->ni", discrete_a, state) + np.einsum("nij,nj->ni", discrete_b, delta_u)

        def run_numpy_jac(
            steps: int = jac_steps,
            batch: int = batch,
            state_np: np.ndarray = state_np,
            control_np: np.ndarray = control_np,
            dt: float = dt,
        ) -> None:
            for _ in range(steps):
                for index in range(batch):
                    rate_jacobians(state_np[index], control_np[index], dt)

        def run_refreshed(
            steps: int = jac_steps,
            batch: int = batch,
            state_np: np.ndarray = state_np,
            control_np: np.ndarray = control_np,
            deviation: np.ndarray = deviation,
            delta_u: np.ndarray = delta_u,
            dt: float = dt,
        ) -> None:
            for _ in range(steps):
                for index in range(batch):
                    state_jacobian, input_jacobian = rate_jacobians(state_np[index], control_np[index], dt)
                    step_a, step_b = jac_analytic_to_discrete(state_jacobian, input_jacobian, dt)
                    _ = step_a @ deviation[index] + step_b @ delta_u[index]

        add("numpy_nonlinear", batch, steps, _time_call(run_numpy_nonlinear, warmup=2), "cpu")
        add("numpy_linear_map", batch, steps, _time_call(run_numpy_linear, warmup=2), "cpu")
        add("numpy_jacobian_analytic", batch, jac_steps, _time_call(run_numpy_jac, warmup=jac_warmup), "cpu")
        add("numpy_refreshed_linear", batch, jac_steps, _time_call(run_refreshed, warmup=jac_warmup), "cpu")

        for device in devices:
            state_t = torch.tensor(state_np, dtype=torch.float64, device=device)
            control_t = torch.tensor(control_np, dtype=torch.float64, device=device)
            map_a = torch.tensor(discrete_a, dtype=torch.float64, device=device)
            map_b = torch.tensor(discrete_b, dtype=torch.float64, device=device)
            deviation_t = torch.zeros_like(state_t)
            delta_u_t = torch.zeros_like(control_t)
            placement = "cuda_resident" if device.type == "cuda" else "cpu"

            def run_torch_nonlinear(
                state_t: torch.Tensor = state_t,
                control_t: torch.Tensor = control_t,
                device: torch.device = device,
                steps: int = steps,
            ) -> None:
                state = state_t
                for _ in range(steps):
                    state = step_nonlinear_torch(state, control_t)
                _sync_if_cuda(device)

            def run_torch_linear(
                deviation_t: torch.Tensor = deviation_t,
                delta_u_t: torch.Tensor = delta_u_t,
                map_a: torch.Tensor = map_a,
                map_b: torch.Tensor = map_b,
                device: torch.device = device,
                steps: int = steps,
            ) -> None:
                state = deviation_t
                for _ in range(steps):
                    state = torch.bmm(map_a, state.unsqueeze(-1)).squeeze(-1) + torch.bmm(
                        map_b, delta_u_t.unsqueeze(-1)
                    ).squeeze(-1)
                _sync_if_cuda(device)

            def run_autograd(
                state_t: torch.Tensor = state_t,
                control_t: torch.Tensor = control_t,
                device: torch.device = device,
                steps: int = jac_steps,
                batch: int = batch,
            ) -> None:
                for _ in range(steps):
                    for index in range(batch):
                        jac_autograd_torch(state_t[index], control_t[index])
                _sync_if_cuda(device)

            nonlinear_name = "torch_cpu_nonlinear" if device.type == "cpu" else "cuda_resident_nonlinear"
            linear_name = "torch_cpu_linear_map" if device.type == "cpu" else "cuda_resident_linear_map"
            jac_name = "torch_cpu_jacobian_autograd" if device.type == "cpu" else "cuda_jacobian_autograd"
            add(nonlinear_name, batch, steps, _time_call(run_torch_nonlinear, warmup=2), placement)
            add(linear_name, batch, steps, _time_call(run_torch_linear, warmup=2), placement)
            add(jac_name, batch, jac_steps, _time_call(run_autograd, warmup=jac_warmup), placement)

            if device.type == "cuda":
                host_state = torch.tensor(state_np, dtype=torch.float64)
                host_control = torch.tensor(control_np, dtype=torch.float64)
                host_dev = torch.zeros_like(host_state)
                host_du = torch.zeros_like(host_control)

                def run_transfer_nonlinear(
                    host_state: torch.Tensor = host_state,
                    host_control: torch.Tensor = host_control,
                    device: torch.device = device,
                    steps: int = steps,
                ) -> None:
                    state = host_state
                    for _ in range(steps):
                        state_d = state.to(device, non_blocking=False)
                        control_d = host_control.to(device, non_blocking=False)
                        state_d = step_nonlinear_torch(state_d, control_d)
                        torch.cuda.synchronize(device)
                        state = state_d.to("cpu")

                def run_transfer_linear(
                    host_dev: torch.Tensor = host_dev,
                    host_du: torch.Tensor = host_du,
                    map_a: torch.Tensor = map_a,
                    map_b: torch.Tensor = map_b,
                    device: torch.device = device,
                    steps: int = steps,
                ) -> None:
                    state = host_dev
                    for _ in range(steps):
                        state_d = state.to(device, non_blocking=False)
                        du_d = host_du.to(device, non_blocking=False)
                        state_d = torch.bmm(map_a, state_d.unsqueeze(-1)).squeeze(-1) + torch.bmm(
                            map_b, du_d.unsqueeze(-1)
                        ).squeeze(-1)
                        torch.cuda.synchronize(device)
                        state = state_d.to("cpu")

                def run_analytic_to_cuda(
                    steps: int = jac_steps,
                    device: torch.device = device,
                    batch: int = batch,
                    state_np: np.ndarray = state_np,
                    control_np: np.ndarray = control_np,
                    dt: float = dt,
                ) -> None:
                    for _ in range(steps):
                        for index in range(batch):
                            state_jacobian, input_jacobian = rate_jacobians(state_np[index], control_np[index], dt)
                            _ = torch.tensor(state_jacobian, dtype=torch.float64, device=device)
                            _ = torch.tensor(input_jacobian, dtype=torch.float64, device=device)
                    torch.cuda.synchronize(device)

                add(
                    "cuda_transfer_nonlinear",
                    batch,
                    steps,
                    _time_call(run_transfer_nonlinear, warmup=1),
                    "cuda_transfer",
                )
                add(
                    "cuda_transfer_linear_map",
                    batch,
                    steps,
                    _time_call(run_transfer_linear, warmup=1),
                    "cuda_transfer",
                )
                add(
                    "cuda_jacobian_analytic",
                    batch,
                    jac_steps,
                    _time_call(run_analytic_to_cuda, warmup=jac_warmup),
                    "cuda_transfer",
                )

        print(f"timed batch {batch}", flush=True)
    return records


def one_step_taylor_check(
    rate_jacobians: Callable[[np.ndarray, np.ndarray, float], tuple[np.ndarray, np.ndarray]],
    reference: np.ndarray,
    controls: np.ndarray,
) -> dict[str, float]:
    """Analytic discrete Jacobian against autograd, and the one-step remainder."""
    rng = np.random.default_rng(1)
    dt = DT_REF
    indices = np.linspace(0, controls.shape[0] - 1, 6, dtype=int)
    jac_gaps: list[float] = []
    remainders: list[float] = []
    for index in indices:
        state = reference[index]
        control = controls[index]
        state_jacobian, input_jacobian = rate_jacobians(state, control, dt)
        discrete_a, discrete_b = jac_analytic_to_discrete(state_jacobian, input_jacobian, dt)
        auto_a, auto_b = jac_autograd_torch(
            torch.tensor(state, dtype=torch.float64),
            torch.tensor(control, dtype=torch.float64),
            dt=dt,
        )
        jac_gaps.append(
            float(
                max(
                    np.max(np.abs(discrete_a - auto_a.detach().numpy())),
                    np.max(np.abs(discrete_b - auto_b.detach().numpy())),
                )
            )
        )
        delta_x = rng.normal(0.0, 1e-4, size=13)
        quat = state[6:10]
        delta_x[6:10] -= quat * np.dot(quat, delta_x[6:10])
        delta_u = rng.normal(0.0, 1e-4, size=4)
        perturbed = state + delta_x
        perturbed[6:10] /= np.linalg.norm(perturbed[6:10])
        # The derivative is of the un-normalized map. Compare before renormalizing.
        base = step_one(state, control, dt)
        truth = step_one(perturbed, control + delta_u, dt)
        linear = base + discrete_a @ delta_x + discrete_b @ delta_u
        remainders.append(float(np.linalg.norm(truth - linear)))
    return {
        "analytic_vs_autograd_inf": float(np.max(jac_gaps)),
        "one_step_remainder_max": float(np.max(remainders)),
        "delta_scale": 1e-4,
        "n_states": float(len(indices)),
    }


# One IEEE column is about 3.5 in. Figures are drawn at that width so the
# type is not shrunk when the PDF places them at full column width.
COLUMN_IN = 3.45


def _save_column(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG / name, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def _legend_below(axis: plt.Axes, handles: list[plt.Line2D] | None = None, ncol: int = 1) -> None:
    kwargs: dict[str, object] = {
        "fontsize": 6.5,
        "loc": "upper center",
        "bbox_to_anchor": (0.5, -0.32),
        "frameon": False,
        "ncol": ncol,
    }
    if handles is None:
        axis.legend(**kwargs)
    else:
        axis.legend(handles=handles, **kwargs)


def plot_scenarios(references: dict[str, tuple[np.ndarray, np.ndarray]]) -> None:
    fig = plt.figure(figsize=(COLUMN_IN, 3.5))
    axes = fig.add_subplot(111, projection="3d")
    for kind, (times, states) in references.items():
        stride = max(1, len(times) // 400)
        axes.plot(
            states[::stride, 0],
            states[::stride, 1],
            states[::stride, 2],
            label=SCENARIO_LABELS[kind],
            lw=1.6,
        )
    axes.set_xlabel("East, x (m)", labelpad=8)
    axes.set_ylabel("North, y (m)", labelpad=8)
    axes.set_zlabel("Up, z (m)", labelpad=6)
    axes.tick_params(labelsize=6.5, pad=1)
    handles, labels = axes.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.48, 0.99), ncol=2, fontsize=6.5, frameon=False)
    # The z label sits just outside a full-width 3D axes, so the axes is inset.
    fig.subplots_adjust(left=0.02, right=0.86, bottom=0.14, top=0.78)
    fig.savefig(FIG / "scenarios_3d.png", dpi=220)
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(COLUMN_IN, 5.6), sharex=True)
    for kind, (times, states) in references.items():
        controls = controls_on_grid(kind, DT_REF)
        thrust = controls.sum(axis=1)
        if kind == "roll_reversal":
            differential = controls[:, 1] + controls[:, 2] - controls[:, 0] - controls[:, 3]
        else:
            differential = controls[:, 0] + controls[:, 2] - controls[:, 1] - controls[:, 3]
        stamp = DT_REF * np.arange(thrust.shape[0])
        stride = max(1, len(stamp) // 500)
        label = SCENARIO_LABELS[kind]
        axes[0].plot(stamp[::stride], thrust[::stride], label=label, lw=1.5)
        axes[1].plot(stamp[::stride], differential[::stride], label=label, lw=1.5)
        axes[2].plot(times[::stride], tilt_deg(states[::stride, 6:10]), label=label, lw=1.5)
    axes[0].set_ylabel("Collective thrust (N)")
    axes[1].set_ylabel("Pair difference (N)")
    axes[2].set_ylabel("Tilt (deg)")
    axes[2].set_xlabel("Time from release (s)")
    axes[0].legend(fontsize=6.5, loc="lower center", bbox_to_anchor=(0.5, 1.05), ncol=2, frameon=False)
    _save_column(fig, "scenarios_thrust_tilt.png")


def plot_errors(rows: list[dict[str, object]]) -> None:
    palette = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    colors = {kind: palette[index] for index, kind in enumerate(SCENARIOS)}
    styles = (("nonlinear", "-", "Nonlinear step"), ("linear_held", "--", "Jacobian held"))
    shown = [kind for kind in SCENARIOS if kind != "hover"]
    panels = (
        ("pos_rmse_m", "Position RMSE (m)", "error_position.png"),
        ("att_rmse_deg", "Attitude RMSE (deg)", "error_attitude.png"),
    )
    for key, ylabel, filename in panels:
        fig, axis = plt.subplots(figsize=(COLUMN_IN, 3.15))
        for kind in SCENARIOS:
            for method, style, _label in styles:
                subset = [row for row in rows if row["method"] == method and row["scenario"] == kind]
                subset.sort(key=lambda row: float(row["dt"]))
                dts = [float(row["dt"]) * 1e3 for row in subset]
                vals = [float(row[key]) if float(row[key]) > 0.0 else np.nan for row in subset]
                axis.plot(dts, vals, style, color=colors[kind], marker="o", ms=4.5, lw=1.5)
        axis.set_xlabel("Step or hold, Δt (ms)")
        axis.set_ylabel(ylabel)
        axis.set_yscale("log")
        scenario_handles = [
            plt.Line2D([0], [0], color=colors[kind], lw=1.6, label=SCENARIO_LABELS[kind]) for kind in shown
        ]
        method_handles = [
            plt.Line2D([0], [0], color="black", ls=style, marker="o", ms=4.5, label=label)
            for _method, style, label in styles
        ]
        _legend_below(axis, scenario_handles + method_handles)
        _save_column(fig, filename)


PROPAGATION_NAMES = (
    "numpy_nonlinear",
    "torch_cpu_nonlinear",
    "numpy_linear_map",
    "torch_cpu_linear_map",
    "numpy_refreshed_linear",
    "cuda_resident_nonlinear",
    "cuda_transfer_nonlinear",
    "cuda_resident_linear_map",
    "cuda_transfer_linear_map",
)
JACOBIAN_NAMES = (
    "numpy_jacobian_analytic",
    "torch_cpu_jacobian_autograd",
    "cuda_jacobian_analytic",
    "cuda_jacobian_autograd",
)
PRETTY = {
    "numpy_nonlinear": "NumPy nonlinear",
    "torch_cpu_nonlinear": "Torch CPU nonlinear",
    "numpy_linear_map": "NumPy linear map",
    "torch_cpu_linear_map": "Torch CPU linear map",
    "numpy_refreshed_linear": "NumPy Jacobian + map",
    "cuda_resident_nonlinear": "CUDA nonlinear, resident",
    "cuda_transfer_nonlinear": "CUDA nonlinear, transfer",
    "cuda_resident_linear_map": "CUDA linear map, resident",
    "cuda_transfer_linear_map": "CUDA linear map, transfer",
    "numpy_jacobian_analytic": "Analytic Jacobian",
    "torch_cpu_jacobian_autograd": "Autograd Jacobian",
    "cuda_jacobian_analytic": "Analytic Jacobian + H2D",
    "cuda_jacobian_autograd": "Autograd Jacobian, CUDA",
}


def plot_speed(records: list[dict[str, object]]) -> None:
    panels = (
        (PROPAGATION_NAMES, "speed_apply.png"),
        (JACOBIAN_NAMES, "speed_build.png"),
    )
    for names, filename in panels:
        fig, axis = plt.subplots(figsize=(COLUMN_IN, 3.15))
        for name in names:
            rows = [row for row in records if row["name"] == name]
            if not rows:
                continue
            rows.sort(key=lambda row: int(row["batch_size"]))
            axis.loglog(
                [int(row["batch_size"]) for row in rows],
                [float(row["us_per_step_item"]) for row in rows],
                marker="o",
                ms=4.5,
                lw=1.5,
                label=PRETTY[name],
            )
        axis.set_xlabel("Vehicles in the batch")
        axis.set_ylabel("Time per vehicle\nper step (µs)")
        _legend_below(axis)
        _save_column(fig, filename)


def crossover_notes(records: list[dict[str, object]]) -> dict[str, object]:
    def series(name: str) -> dict[int, float]:
        return {int(row["batch_size"]): float(row["us_per_step_item"]) for row in records if row["name"] == name}

    nonlinear = series("numpy_nonlinear")
    linear = series("numpy_linear_map")
    refreshed = series("numpy_refreshed_linear")
    torch_nl = series("torch_cpu_nonlinear")
    torch_lin = series("torch_cpu_linear_map")

    def first_faster(left: dict[int, float], right: dict[int, float]) -> int | None:
        for batch in sorted(left):
            if left[batch] < right[batch]:
                return batch
        return None

    def first_slower(left: dict[int, float], right: dict[int, float]) -> int | None:
        for batch in sorted(left):
            if left[batch] > right[batch]:
                return batch
        return None

    notes: dict[str, object] = {
        "numpy_linear_faster_than_nonlinear_from_batch": first_faster(linear, nonlinear),
        "torch_linear_faster_than_nonlinear_from_batch": first_faster(torch_lin, torch_nl),
        "numpy_refreshed_faster_than_nonlinear_from_batch": first_faster(refreshed, nonlinear),
        "numpy_refreshed_slower_than_nonlinear_from_batch": first_slower(refreshed, nonlinear),
        "ratios_at_max_batch": {},
    }
    max_batch = max(nonlinear)
    notes["ratios_at_max_batch"] = {
        "batch": max_batch,
        "numpy_nonlinear_us": nonlinear[max_batch],
        "numpy_linear_us": linear[max_batch],
        "numpy_refreshed_us": refreshed[max_batch],
        "torch_nonlinear_us": torch_nl[max_batch],
        "torch_linear_us": torch_lin[max_batch],
        "linear_over_nonlinear": linear[max_batch] / nonlinear[max_batch],
        "refreshed_over_nonlinear": refreshed[max_batch] / nonlinear[max_batch],
    }
    if any(row["name"] == "cuda_resident_nonlinear" for row in records):
        resident = series("cuda_resident_nonlinear")
        transfer = series("cuda_transfer_nonlinear")
        resident_lin = series("cuda_resident_linear_map")
        notes["cuda_resident_nonlinear_faster_than_cpu_from_batch"] = first_faster(resident, torch_nl)
        notes["cuda_resident_faster_than_transfer_from_batch"] = first_faster(resident, transfer)
        notes["cuda_resident_linear_faster_than_transfer_from_batch"] = first_faster(
            resident_lin, series("cuda_transfer_linear_map")
        )
        notes["ratios_at_max_batch"]["cuda_resident_nonlinear_us"] = resident[max_batch]
        notes["ratios_at_max_batch"]["cuda_transfer_nonlinear_us"] = transfer[max_batch]
    return notes


def fmt(value: float, digits: int = 3) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.{digits}e}"
    return f"{value:.{digits}g}"


def write_tables(errors: list[dict[str, object]], records: list[dict[str, object]], checks: dict[str, float]) -> str:
    lines = ["### Trajectory error", ""]
    lines.append(
        "| Scenario | Hold / step | Method | Position RMSE | Position at 2 s | Attitude RMSE | Attitude at 2 s |"
    )
    lines.append("|---|---:|---|---:|---:|---:|---:|")
    for row in errors:
        lines.append(
            "| {scenario} | {dt_ms:.1f} ms | {method} | {pos} m | {end} m | {att}° | {att_end}° |".format(
                scenario=SCENARIO_LABELS[str(row["scenario"])],
                dt_ms=float(row["dt"]) * 1e3,
                method="nonlinear" if row["method"] == "nonlinear" else "linear, Jacobian held",
                pos=fmt(float(row["pos_rmse_m"])),
                end=fmt(float(row["pos_horizon_m"])),
                att=fmt(float(row["att_rmse_deg"])),
                att_end=fmt(float(row["att_horizon_deg"])),
            )
        )
    lines.extend(["", "### Speed", ""])
    lines.append("| Method | Batch | µs / (step·item) | (step·item) / s |")
    lines.append("|---|---:|---:|---:|")
    for row in records:
        lines.append(
            "| {name} | {batch} | {us} | {rate} |".format(
                name=PRETTY[str(row["name"])],
                batch=int(row["batch_size"]),
                us=fmt(float(row["us_per_step_item"])),
                rate=fmt(float(row["items_per_s"]), 4),
            )
        )
    lines.extend(
        [
            "",
            "### Jacobian agreement on the pitch-pulse reference",
            "",
            f"- Analytic discrete Jacobian vs autograd, max abs: {checks['analytic_vs_autograd_inf']:.3e}",
            f"- One-step linear remainder at δ ~ {checks['delta_scale']:.0e}: {checks['one_step_remainder_max']:.3e}",
            "",
        ]
    )
    text = "\n".join(lines)
    (GENERATED / "tables.md").write_text(text + "\n")
    return text


def style_plots() -> None:
    plt.rcParams.update(
        {
            "font.size": 7,
            "axes.labelsize": 7,
            "axes.titlesize": 7,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "legend.fontsize": 6.5,
            "axes.grid": True,
            "grid.alpha": 0.35,
            "figure.dpi": 140,
            "savefig.dpi": 220,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "axes.labelpad": 2,
        }
    )


def main() -> None:
    FIG.mkdir(exist_ok=True)
    GENERATED.mkdir(exist_ok=True)
    style_plots()
    hardware = hardware_record()
    print("building analytic Jacobians", flush=True)
    rate_jacobians, symbolic_f = build_jacobians()
    hover_u = np.full(4, hover_thrust())
    hover_x = initial_state()
    symbolic = symbolic_f(hover_x, hover_u, DT_REF)
    block = step_one(hover_x, hover_u, DT_REF)
    hover_gap = float(np.max(np.abs(symbolic - block)))
    print(f"hover |f_sym - f_np|_inf = {hover_gap}", flush=True)

    references: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    errors: list[dict[str, object]] = []
    for kind in SCENARIOS:
        print(f"reference {kind}", flush=True)
        times, states = rollout_nonlinear(kind, DT_REF)
        references[kind] = (times, states)
        for dt in COARSE_DTS:
            _, coarse = rollout_nonlinear(kind, dt)
            _, linear = rollout_linear_held(kind, dt, rate_jacobians)
            for method, traj in (("nonlinear", coarse), ("linear_held", linear)):
                row: dict[str, object] = {"scenario": kind, "dt": dt, "method": method}
                row.update(trajectory_errors(traj, states, dt))
                errors.append(row)
                print(
                    f"  {kind} dt={dt * 1e3:.1f} ms {method}: "
                    f"pos {float(row['pos_rmse_m']):.3e} m, att {float(row['att_rmse_deg']):.3e} deg",
                    flush=True,
                )

    scenario_summary: dict[str, dict[str, object]] = {}
    for kind, (times, states) in references.items():
        scenario_summary[kind] = {
            "final_position_m": [float(value) for value in states[-1, 0:3]],
            "max_tilt_deg": float(np.max(tilt_deg(states[:, 6:10]))),
            "path_length_m": float(np.sum(np.linalg.norm(np.diff(states[:, 0:3], axis=0), axis=1))),
            "duration_s": float(times[-1]),
        }

    pitch_controls = controls_on_grid("pitch_pulse", DT_REF)
    checks = one_step_taylor_check(rate_jacobians, references["pitch_pulse"][1], pitch_controls)
    print("checks", checks, flush=True)
    plot_scenarios(references)
    plot_errors(errors)
    print("timing", flush=True)
    records = speed_records(rate_jacobians)
    plot_speed(records)
    notes = crossover_notes(records)
    payload = {
        "hardware": hardware,
        "hover_symbolic_gap_inf": hover_gap,
        "dt_ref_s": DT_REF,
        "horizon_s": HORIZON,
        "coarse_dts_s": list(COARSE_DTS),
        "checks": checks,
        "scenarios": scenario_summary,
        "errors": errors,
        "speed": records,
        "crossover": notes,
    }
    (HERE / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    write_tables(errors, records, checks)
    print("wrote results.json and figures", flush=True)


if __name__ == "__main__":
    main()
