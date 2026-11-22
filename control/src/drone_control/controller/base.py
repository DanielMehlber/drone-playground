"""Types shared by every control law, and the controller that dispatches to one."""

from dataclasses import dataclass
from typing import Protocol, assert_never

from geometry_msgs.msg import Vector3
from sensor_msgs.msg import FluidPressure, Imu, MagneticField, NavSatFix

type RotorSpeeds = tuple[float, float, float, float]
"""Rotor i in rad/s. Indices 0 and 1 are CCW, 2 and 3 are CW."""

STOPPED: RotorSpeeds = (0.0, 0.0, 0.0, 0.0)


@dataclass
class SensorState:
    """Newest sample of each sensor, or None until the first one arrives."""

    imu: Imu | None = None
    mag: MagneticField | None = None
    baro: FluidPressure | None = None
    gnss: NavSatFix | None = None


@dataclass(frozen=True, slots=True)
class Altitude:
    meters: float


@dataclass(frozen=True, slots=True)
class Velocity:
    vector: Vector3  # forward, right, down


@dataclass(frozen=True, slots=True)
class Acceleration:
    vector: Vector3  # forward, right, down


type TargetState = Altitude | Velocity | Acceleration
"""What the controller is trying to achieve."""


class ControlLaw(Protocol):
    def altitude_control(self, state: SensorState, altitude: float) -> RotorSpeeds: ...

    def velocity_control(self, state: SensorState, velocity: Vector3) -> RotorSpeeds: ...

    def acceleration_control(self, state: SensorState, acceleration: Vector3) -> RotorSpeeds: ...


class Controller:
    def __init__(self, control_law: ControlLaw) -> None:
        self._control_law = control_law

    def step(self, state: SensorState, target: TargetState) -> RotorSpeeds:
        match target:
            case Altitude(meters):
                return self._control_law.altitude_control(state, meters)
            case Velocity(vector):
                return self._control_law.velocity_control(state, vector)
            case Acceleration(vector):
                return self._control_law.acceleration_control(state, vector)
            case _:
                assert_never(target)
