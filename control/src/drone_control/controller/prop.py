from dataclasses import dataclass

from geometry_msgs.msg import Vector3

from drone_control.controller.barometer import air_pressure_to_altitude
from drone_control.controller.base import STOPPED, RotorSpeeds, SensorState


@dataclass(frozen=True, slots=True)
class PropControlLaw:
    k: float
    min_speed: float
    max_speed: float

    def altitude_control(self, state: SensorState, altitude: float) -> RotorSpeeds:
        if state.baro is None:
            return STOPPED
        current_alt = air_pressure_to_altitude(float(state.baro.fluid_pressure))
        error = current_alt - altitude
        strength = self.k * error
        return (strength, strength, strength, strength)

    def velocity_control(self, state: SensorState, velocity: Vector3) -> RotorSpeeds:
        return STOPPED

    def acceleration_control(self, state: SensorState, acceleration: Vector3) -> RotorSpeeds:
        return STOPPED
