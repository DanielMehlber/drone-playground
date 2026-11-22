#!/usr/bin/env bash
# Sensors flow Gazebo to ROS. Rotor speeds flow ROS to Gazebo.
# The controller never includes a Gazebo type. It only sees these ROS topics.
set -euo pipefail
set +u
source /opt/ros/jazzy/setup.bash
set -u

exec ros2 run ros_gz_bridge parameter_bridge \
  /imu@sensor_msgs/msg/Imu[gz.msgs.IMU \
  /magnetometer@sensor_msgs/msg/MagneticField[gz.msgs.Magnetometer \
  /air_pressure@sensor_msgs/msg/FluidPressure[gz.msgs.FluidPressure \
  /navsat@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat \
  /X3/gazebo/command/motor_speed@actuator_msgs/msg/Actuators]gz.msgs.Actuators
