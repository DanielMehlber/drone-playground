"""Inner loop.

Listens to the four drone sensors, runs `Controller.step`, and publishes
the four rotor speeds that step returns.

`/X3/gazebo/command/motor_speed` carries `actuator_msgs/Actuators`.
`velocity[i]` is rotor i in rad/s. Indices 0 and 1 are CCW, 2 and 3 are CW.
The plant caps each speed at 800 rad/s.
"""

import rclpy
from actuator_msgs.msg import Actuators
from rclpy.context import Context
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.utilities import try_shutdown
from sensor_msgs.msg import FluidPressure, Imu, MagneticField, NavSatFix

from drone_control.controller import (
    Altitude,
    BangBangControlLaw,
    ControlLaw,
    Controller,
    PropControlLaw,
    RotorSpeeds,
    SensorState,
    TargetState,
)

IMU_TOPIC = "/imu"
MAG_TOPIC = "/magnetometer"
BARO_TOPIC = "/air_pressure"
GNSS_TOPIC = "/navsat"
MOTOR_TOPIC = "/X3/gazebo/command/motor_speed"

QOS_DEPTH = 10


class ControllerNode(Node):
    def __init__(
        self,
        *,
        context: Context | None = None,
        parameter_overrides: list[Parameter] | None = None,
    ) -> None:
        super().__init__("controller", context=context, parameter_overrides=parameter_overrides)

        self.declare_parameter("control_law", "prop")
        self.declare_parameter("k", 10.0)
        self.declare_parameter("min_speed", 650.0)
        self.declare_parameter("max_speed", 700.0)
        self.declare_parameter("target_altitude", 10.0)

        self._controller = Controller(self._control_law_from_parameters())
        self._target: TargetState = Altitude(self._float_parameter("target_altitude"))
        self._state = SensorState()

        self._motors = self.create_publisher(Actuators, MOTOR_TOPIC, QOS_DEPTH)
        self.create_subscription(Imu, IMU_TOPIC, self._on_imu, QOS_DEPTH)
        self.create_subscription(MagneticField, MAG_TOPIC, self._on_mag, QOS_DEPTH)
        self.create_subscription(FluidPressure, BARO_TOPIC, self._on_baro, QOS_DEPTH)
        self.create_subscription(NavSatFix, GNSS_TOPIC, self._on_gnss, QOS_DEPTH)

        log = self.get_logger()
        log.info(f"listening on {IMU_TOPIC}, {MAG_TOPIC}, {BARO_TOPIC}, {GNSS_TOPIC}")
        log.info(f"publishing rotor speeds on {MOTOR_TOPIC}")

    def _float_parameter(self, name: str) -> float:
        return float(self.get_parameter(name).value)

    def _control_law_from_parameters(self) -> ControlLaw:
        name = str(self.get_parameter("control_law").value)
        min_speed = self._float_parameter("min_speed")
        max_speed = self._float_parameter("max_speed")
        match name:
            case "prop":
                return PropControlLaw(k=self._float_parameter("k"), min_speed=min_speed, max_speed=max_speed)
            case "bang":
                return BangBangControlLaw(min_speed=min_speed, max_speed=max_speed)
            case _:
                msg = f"unknown control_law {name!r}, expected 'prop' or 'bang'"
                raise ValueError(msg)

    def _on_imu(self, msg: Imu) -> None:
        self._state.imu = msg
        self._step()

    def _on_mag(self, msg: MagneticField) -> None:
        self._state.mag = msg
        self._step()

    def _on_baro(self, msg: FluidPressure) -> None:
        self._state.baro = msg
        self._step()

    def _on_gnss(self, msg: NavSatFix) -> None:
        self._state.gnss = msg
        self._step()

    def _step(self) -> None:
        self._motors.publish(actuator_command(self._controller.step(self._state, self._target)))


def actuator_command(speeds: RotorSpeeds) -> Actuators:
    command = Actuators()
    command.velocity = [float(speed) for speed in speeds]
    return command


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = ControllerNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        try_shutdown()
