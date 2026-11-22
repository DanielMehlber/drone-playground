---
type: concept
module: control
tags:
  - concept
  - control
status: article
aliases:
  - PID
---

# PID control

A PID controller computes a command from three terms on an error: proportional, integral, and derivative. Nicolas Minorsky wrote the analysis for automatic ship steering in 1922. Ziegler and Nichols published a practical tuning procedure in 1942. It is still the default industrial loop, and it is still the default rate loop on a [[Quadrotor]].

## The problem

You need a command that grows when the error grows, that removes a constant bias such as weight or a motor that is a bit weak, and that damps overshoot. Those are P, I, and D. The derivative is usually taken on the measurement, so a step in the setpoint does not kick the motors.

## What you use it for

On this aircraft the rate loop wants all three terms. The plant from torque to angular rate is close to first order, which is why people learn gains there. Attitude and position are often a P on angle or position plus a damping term on rate or velocity. The integrator at hover is what holds the weight.

[[Anti-windup]] matters the first time a motor saturates and the integrator keeps climbing. [[Linear quadratic regulator|LQR]] and [[Incremental nonlinear dynamic inversion|INDI]] are what you compare against this baseline later. Keep the PID. It is the number the clever controller has to beat.

## See also

- [[Cascade control]]
- [[Wrench]]
