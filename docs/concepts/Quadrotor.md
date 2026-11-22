---
type: concept
module: simulation
tags:
  - concept
  - simulation
status: article
aliases:
  - quadcopter
  - multirotor
---

# Quadrotor

A quadrotor is an aircraft that lifts itself with four rotors. The idea is old. The Bréguet-Richet Gyroplane made short tethered hops in 1907, and George de Bothezat flew a large four-rotor machine for the US Army in 1922. Small electric quadrotors became practical in the late 1990s and 2000s, once batteries, motors, and chips were light enough. The research wave behind today's papers ran roughly from 2005 to 2015, at places such as the University of Pennsylvania and ETH Zurich.

## The problem

A wing needs speed or a runway. A helicopter solves that with one big rotor and a tail rotor, and the mechanics are complicated. Four smaller rotors can be fixed in place. You steer by spinning them at different speeds, which a computer can do and a person with a stick cannot, at least not well.

## What you use it for

Each rotor pushes air downward and so pushes the aircraft upward. Tilt happens when one side pushes harder than the other. Yaw, the turn left or right, happens because the motors spin in alternating directions and their drag torques cancel or add. There is no rudder and no swashplate.

This playground simulates one quadrotor, the X3 mass and rotor layout in [[Simulation]], as a [[Rigid-body quadrotor]]. Several vehicles later is the same idea with more than one body in [[Gazebo]].

## See also

- [[Flight controller]]
- [[Motor model]]
- [[Control allocation]]
