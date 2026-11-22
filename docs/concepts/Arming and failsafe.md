---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# Arming and failsafe

Arming is the explicit switch from "motors must stay still" to "motors may spin." A failsafe is the rule for what the [[Autopilot]] does when that trust breaks: a lost link, a crashed estimator, a low battery, or a stream of commands that stops arriving.

## The problem

Propellers injure people. A bug in a new controller, or a laptop that goes to sleep, must not leave the motors running with nobody in charge. The arming flag is the gate. The failsafe is the path back to a dull outcome, usually disarm on the bench and a landing in the air.

## Background

The pattern is older than small drones. Crewed autopilots have had disconnect and reversion rules for decades. [[PX4 Autopilot|PX4]] and [[QGroundControl]] keep a person, or a ground station, in the arming decision on purpose.

## In this playground

There is no arming flag. The motors spin when [[Control]] publishes non-zero speeds, and they stay stopped while that topic is silent. A timeout that sends zeros, or stops publishing, is the failsafe you add in the same package. On a [[PX4 Autopilot]] vehicle, arming is a separate switch. That switch is not in this setup.

## See also

- [[Flight controller]]
- [[Ground control station]]
