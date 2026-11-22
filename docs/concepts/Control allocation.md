---
type: concept
module: allocation
tags:
  - concept
  - allocation
status: article
---

# Control allocation

Control allocation turns a desired [[Wrench]] into actuator commands. For a [[Quadrotor]] in an X the map is square: thrust and three torques in, four motor commands out. Each row of the geometry matrix is one motor's contribution, fixed by arm length and spin direction. The first solution is the inverse of that matrix. The subject is a standard chapter in aircraft control and has been applied to multirotors since the research literature of the 2000s.

## The problem

[[Control]] should not contain a diagram of which motor is clockwise. The loops speak force and torque. A separate map can be tested with a constant wrench and no flight. When a command would leave the legal range, [[Saturation and desaturation]] decides what to sacrifice. Giving up yaw before giving up thrust is the usual choice, because a loss of yaw is gentler than a loss of lift.

## In this playground

The map lives inside [[Control]], for the rotor positions in [[Simulation]]. The [[Motor model]] in [[Gazebo]] is the same geometry read in the other direction. If the two disagree on order, the aircraft flips on the first command and the linear algebra can still be correct.

## See also

- [[Electronic speed controller]]
- [[Anti-windup]]
