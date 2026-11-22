---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# uORB

uORB is the publish-subscribe bus inside [[PX4 Autopilot|PX4]]. Modules in one process, the estimator, the controllers, the drivers, pass each other small C structs on named topics. The name is a nod to CORBA's "object request broker," scaled down to a microcontroller. It has been the way PX4 modules talk since the early flight stack.

## The problem

A flight controller is one realtime process with many jobs. Function calls between all of them become a knot. A tiny bus lets a gyro driver publish and anyone subscribe, without those modules including each other's code.

## In this playground

Not in the running system. You meet uORB when a loop moves into [[PX4 Autopilot]] firmware. Until then the sensors and the rotor speeds are ROS topics. See [[Control]].

## See also

- [[EKF2]]
- [[Offboard mode]]
