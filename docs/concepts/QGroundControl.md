---
type: concept
module: playground
tags:
  - concept
  - playground
status: article
aliases:
  - QGC
---

# QGroundControl

QGroundControl is a [[Ground control station]] for vehicles that speak [[MAVLink]]. It grew up with [[PX4 Autopilot|PX4]] and has been the everyday operator window for that stack since the mid-2010s. You see attitude, position, and mode, and you arm, disarm, and take back manual control.

## The problem

Plots of a controller are not a picture of an aircraft in a field, and they are not a safe arming switch. Someone needs a window whose job is "is it flying, and can I stop it."

## In this playground

Not used. Nothing in this setup speaks [[MAVLink]]. [[Foxglove]] plots the ROS topics if you want a window. QGroundControl is the ground station you would add with a [[PX4 Autopilot]] vehicle.

## See also

- [[Foxglove]]
- [[Arming and failsafe]]
