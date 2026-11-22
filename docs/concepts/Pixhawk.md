---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# Pixhawk

Pixhawk is an open standard for [[Flight controller]] boards, and also the name of the first widely used board that followed it. The first Pixhawk appeared around 2013, out of the same ETH Zurich work as [[PX4 Autopilot|PX4]] and [[MAVLink]]. The standard is now looked after so that more than one company can sell a compatible board.

## The problem

An autopilot that only runs on one hand-built circuit cannot be shared. A standard says where the [[IMU]] sits, which connectors talk to [[GNSS]] and to the [[Electronic speed controller|speed controllers]], and which microcontroller the software expects. PX4 and ArduPilot can then target that family.

## In this playground

There is no board. [[Gazebo]] publishes the sensors and accepts the rotor speeds a Pixhawk would own. A node written against those ROS topics has a place to go later, usually after the fast loop moves into firmware.

## See also

- [[Flight controller]]
- [[X500]]
