---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Covariance

Covariance is a table of how uncertain a vector is, and of which errors move together. The diagonal is the variance of each component, the square of a typical error. Off-diagonal entries say "when x is wrong, y tends to be wrong the same way." A Gaussian estimate is a mean plus a covariance. That is the state a [[Kalman filter]] carries.

## The problem

A position without an uncertainty cannot be fused with another sensor. You would not know whether to believe the [[GNSS]] fix or the integrated [[IMU]]. The covariance is the filter's own answer to "how sure am I," and it has to be honest. An overconfident covariance ignores good measurements. An inflated one chatters.

## In this playground

`sensor_msgs/Imu` and `NavSatFix` carry covariance blocks. Those numbers are a starting R for an update, if you trust them. Plot a diagonal element next to the squared [[Innovation]] to see whether the filter's doubt matches its mistakes.

## See also

- [[Mahalanobis gate]]
- [[Sensor noise]]
