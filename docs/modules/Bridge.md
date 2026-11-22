---
type: module
module: playground
tags:
  - module
---

# Bridge

This repo no longer runs a Micro XRCE-DDS agent. Gazebo and the controller meet through `ros_gz_bridge`, started by `sim/run-bridge.sh`. Sensors move from Gazebo to ROS. Rotor speeds move from ROS to Gazebo.

[[Micro XRCE-DDS]] remains the way a [[PX4 Autopilot]] flight controller joins a ROS graph. It is background, not a container here.

## See also

- [[Simulation]]
- [[ROS 2]]
