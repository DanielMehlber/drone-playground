---
type: concept
module: allocation
tags:
  - concept
  - allocation
status: article
aliases:
  - ESC
---

# Electronic speed controller

An electronic speed controller, an ESC, is the circuit between a command and a brushless motor. It switches the motor windings so the rotor spins at the speed you asked for. Hobby radio-control models have used ESCs since the 1990s. A [[Quadrotor]] has one per motor, sometimes four chips on one board.

## The problem

A [[Flight controller]] cannot push the amps a propeller motor draws, and it should not have to know the winding pattern. The ESC takes a small signal and produces the large one. The signal in this playground is a normalized command from 0 to 1, the same idea as a throttle percentage.

## In this playground

[[Gazebo]] includes the ESC and the motor as a [[Motor model]]. [[Control]] will publish four speeds in rad/s. You do not model the transistors. You do have to know the order of the four numbers, because each number belongs to one physical motor.

## See also

- [[Control allocation]]
- [[X500]]
