---
type: concept
module: control
tags:
  - concept
  - control
status: article
aliases:
  - LQR
---

# Linear quadratic regulator

A linear quadratic regulator is a state-feedback gain chosen by minimizing a quadratic cost on state error and on actuator effort. It is part of the optimal-control theory Rudolf Kálmán and others set out around 1960, the same era as the [[Kalman filter]]. You pick two weight matrices, Q and R. The algebra returns a gain matrix K. The command is −K times the state error.

## The problem

[[PID control]] has a handful of gains and no story for coupling between axes. LQR takes a linear model, including coupling, and returns every gain at once, with an explicit trade between "be accurate" and "spend actuator." The result is only as good as the linear model, and the weights are still a choice. It is not a tuning-free controller.

## In this playground

Linearize the [[Rigid-body quadrotor]] near hover and try LQR as an attitude or position alternative inside [[Control]]. Keep the same rotor-speed output. A useful comparison is the same hover flown by PID and by LQR, plotted in [[Foxglove]], on the same mass.

## See also

- [[Cascade control]]
- [[Covariance]]
