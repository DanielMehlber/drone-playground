---
type: concept
module: control
tags:
  - concept
  - control
status: article
---

# Cascade control

Cascade control is several feedback loops in a nest. The outer loop's output is the inner loop's setpoint. On a [[Quadrotor]] the usual nest is position, then velocity, then attitude, then angular rate, then motors. Each loop is allowed to assume the one inside it has already done its job, which is true only when the inner loop is several times faster.

The structure is older than drones. Process control used cascaded loops through the twentieth century. [[PX4 Autopilot|PX4]] and ArduPilot both fly this way. Papers that "replace the controller" usually replace one layer and leave the rest.

## The problem

One loop from position error all the way to motor speed is hard to tune, because every gain affects every timescale. Splitting timescales lets you tune the rate loop on the bench, then attitude, then position, and stop when the layer you are touching misbehaves.

## In this playground

[[Control]] is one process with those loops, so the rate loop is not waiting on a network hop. The first version of each loop is [[PID control]]. The mixer sits under the rate loop, in the same process: a desired force and torque become four speeds before the plant moves.

## See also

- [[Geometric attitude control]]
- [[Flight controller]]
