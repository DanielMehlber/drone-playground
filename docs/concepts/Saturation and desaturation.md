---
type: concept
module: allocation
tags:
  - concept
  - allocation
status: article
---

# Saturation and desaturation

Saturation is an actuator at its stop: a motor command below 0 or above 1. Desaturation is the repair, shifting or scaling the whole command so every motor is back inside range while keeping as much of the requested [[Wrench]] as possible. [[PX4 Autopilot|PX4]]'s control allocator has done a version of this for years. The 1.14 release in 2023 made that allocator the standard path and retired the older static mixer files.

## The problem

A naive clip of each motor, one by one, changes the torque you did not mean to change. You asked for thrust and a roll. After clipping you have less roll and also a yaw you never asked for. A desaturation step gives the loss a priority. Thrust is usually last to give up, because the alternative is falling.

## In this playground

Implement the inverse mixer in [[Allocation]] first, with commands that fit. Add desaturation when a unit test wrench does not fit in `[0, 1]`. Report the wrench you actually achieved if [[Anti-windup]] in [[Control]] needs it.

## See also

- [[Control allocation]]
- [[Motor model]]
