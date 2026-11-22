---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# MAVLink

MAVLink is a small binary message protocol for drones and the laptops that fly them. Lorenz Meier designed it in 2009 as part of the PIXHAWK work at ETH Zurich, the same line as [[PX4 Autopilot|PX4]]. Messages cover heartbeat, attitude, GPS, and commands such as arm and set-mode. The packets are compact enough for a radio.

## The problem

A person with [[QGroundControl]] needs to see the aircraft and to arm it. That traffic is older than [[ROS 2]] and still separate from it. Radios and ground stations speak MAVLink. Companion computers increasingly speak [[DDS]]. PX4 speaks both.

## In this playground

Nothing here speaks MAVLink. The controller speaks ROS. MAVLink is the protocol a [[Ground control station]] uses with a [[PX4 Autopilot]] vehicle, which this setup does not run.

## See also

- [[Ground control station]]
- [[Arming and failsafe]]
