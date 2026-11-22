---
type: concept
module: simulation
tags:
  - concept
  - simulation
status: article
---

# Motor model

A first motor model says thrust is proportional to rotation speed squared, and speed follows the command through a first-order lag. Drag torque about the shaft is proportional to thrust. That algebraic model has been the standard simple plant in quadrotor papers since the 2000s. Real motors add voltage limits, battery sag, and a faster electrical time constant.

## The problem

[[Allocation]] outputs a normalized command. The aircraft feels a force a few milliseconds later. If your mixer assumes a different gain or a different motor order than the simulator, the closed loop is unstable for a boring reason.

## In this playground

[[Gazebo]] owns this model for the quadrotor in [[Simulation]]. Thrust is `8.54858e-06 * omega²`. You need the sign of each rotor and the arm geometry before the first non-zero command. A fancier thrust curve is worth it only after hover is repeatable and the rate loop is slow in a way the lag explains.

## See also

- [[Electronic speed controller]]
- [[Saturation and desaturation]]
