---
type: concept
module: control
tags:
  - concept
  - control
status: article
---

# Anti-windup

Anti-windup is the family of fixes for an integrator that keeps accumulating while the actuator is already saturated. The term has been in process-control practice for decades, because PID loops met valve limits long before they met propellers.

## The problem

During a large tilt the motors hit 0 or 1. The attitude error is still nonzero, so the integral term grows. When the aircraft comes back and the motors have room again, that stored integral dumps into the command and the vehicle overshoots. The loop looked fine in a linear simulation that never hit a limit.

## What you use it for

A simple version stops integrating while the command is on a stop, or integrates the difference between the command you asked for and the command [[Allocation]] actually sent. That second version needs the allocator to report what it could do, which is a reason for [[Saturation and desaturation]] to be explicit.

## In this playground

You will meet this in [[Control]] as soon as a rate or attitude test asks for more tilt than the rotors can give. The speed limit is 800 rad/s. Plot the integrator. If it is still moving while a motor is pinned, you are looking at windup.

## See also

- [[PID control]]
- [[Control allocation]]
