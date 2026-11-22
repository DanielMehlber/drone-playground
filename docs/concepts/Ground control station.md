---
type: concept
module: playground
tags:
  - concept
  - playground
status: article
aliases:
  - GCS
---

# Ground control station

A ground control station is the operator's software: a map, instruments, and buttons for arm and mode. The name is from crewed and military aviation. For a small [[Quadrotor]] it is usually a laptop program speaking [[MAVLink]].

## The problem

The [[Companion computer]] is a bad place to put the only stop button. If your new controller locks up, you still want a separate program that can disarm or land. That program is the ground station, and [[PX4 Autopilot|PX4]] expects one to be present before it will arm.

## In this playground

Not part of this setup. [[Foxglove]] can plot the ROS topics. A ground station such as [[QGroundControl]] belongs with a vehicle that speaks [[MAVLink]].

## See also

- [[Foxglove]]
- [[Arming and failsafe]]
