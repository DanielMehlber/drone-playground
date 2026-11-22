---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
aliases:
  - UKF
---

# Unscented Kalman filter

The unscented Kalman filter is a [[Bayes filter]] for nonlinear models that avoids writing Jacobians. Simon Julier and Jeffrey Uhlmann introduced the unscented transform in the mid-1990s, with the filter papers arriving by 1997. It passes a small set of sample points through the real nonlinear function and rebuilds a mean and a [[Covariance]] from the results.

## The problem

An [[Extended Kalman filter]] needs derivatives, and those derivatives are wrong when the estimate is off or the function bends sharply. Attitude and some sensor models bend. The unscented filter spends more CPU per step and is often calmer in those regions. It is still a Gaussian approximation. It will not represent a belief with two peaks.

## In this playground

Write the [[Extended Kalman filter]] first, inside [[Control]]. Replace the predict or an update with the unscented version when a Jacobian is the thing you no longer trust. Keep the same sensor topics. A second algorithm does not need a second ROS interface.

## See also

- [[IMU mechanization]]
- [[Kalman filter]]
