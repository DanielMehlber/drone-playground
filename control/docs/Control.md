---
type: module
module: control
tags:
  - module
---

# Control

One Python process, the `drone_control` package. It reads the sensors and writes four rotor speeds. Rate, attitude, and hover live here, in that order. A route does not. A later node can publish a position or velocity setpoint. This package should subscribe to it. It should not plan the path.

## The problem

The aircraft falls unless the rotors push up with its weight, and it tumbles unless the four speeds differ in the right pattern. That calculation is the inner loop. [[PX4 Autopilot]] already contains one. This project is the loop itself, so PX4 is not in the running system.

## What you use it for

[[Cascade control]] is the usual shape. The rate loop is first, because torque to angular rate is close to a first-order lag and [[PID control]] is enough to see that. Attitude wraps the rate loop. Height and horizontal position wrap attitude, and that combination is hover. [[Geometric attitude control]], [[Incremental nonlinear dynamic inversion]], and [[Linear quadratic regulator]] are later replacements for a loop that already hovers, not a different program.

[[Control allocation]] is the matrix inside this package that turns a desired force and torque into four speeds. It is not a separate ROS node. A network hop between the rate loop and the mixer adds delay for no new idea.

The message is `actuator_msgs/Actuators` on `/X3/gazebo/command/motor_speed`. `velocity` is four numbers in rad/s. The plant's motor order and the 656 rad/s hover guess are in [[Simulation]]. A wrong order flips the vehicle on the first non-zero command.

A filter is the same process, later. [[IMU mechanization]], a [[Complementary filter]], or an [[Extended Kalman filter]] read the same four topics and hand the loops a state. They do not get their own container.

## Layout

| Path | What it is |
|---|---|
| `src/drone_control/controller/` | Control laws and the `Controller` that dispatches on the target. No ROS node code. |
| `src/drone_control/node.py` | The [[rclpy]] node: subscriptions, parameters, motor publisher. |
| `requirements/` | pip-tools lock files, generated from `pyproject.toml`. |

A new law is a class with `altitude_control`, `velocity_control`, and `acceleration_control`, each returning four rotor speeds. It satisfies the `ControlLaw` protocol without inheriting from it. Register it in `ControllerNode._control_law_from_parameters`.

## Run

In the dev container, from `control/`:

```bash
drone-control
drone-control --ros-args -p control_law:=bang -p target_altitude:=5.0
```

Parameters: `control_law` (`prop` or `bang`), `k`, `min_speed`, `max_speed`, `target_altitude`. The defaults are the proportional law with `k = 10` and a 10 m target. Every sensor sample triggers one step and one motor command.

## Tooling

| Command | What it does |
|---|---|
| `make check` | ruff lint and format check, `mypy --strict` |
| `make format` | ruff format and autofix |
| `make lock` | regenerate `requirements/*.txt` after editing dependencies in `pyproject.toml` |
| `make upgrade` | the same, with the newest allowed versions |
| `make sync` | make the venv match `requirements/dev.txt` |

rclpy and the message packages are apt packages in the image, not PyPI dependencies. Keep numpy on apt too: the ROS message extensions are compiled against it. PyTorch is not in the lock files. The dev container installs 2.15.0: the CUDA wheel when the container can see an NVIDIA GPU, and the CPU wheel with the MPS bridge on a Mac.

## Hardware, later

These ROS topics are the lab contract. On a real aircraft the fast rate loop usually moves into [[Flight controller]] firmware, and a small node replaces the Gazebo bridge with an IMU driver and an [[Electronic speed controller]] output. The law stays. The topics are the seam.

## See also

- [[Simulation]]
- [[PID control]]
- [[Cascade control]]
- [[Wrench]]
