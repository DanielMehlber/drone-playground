---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
aliases:
  - EKF
---

# Extended Kalman filter

The extended Kalman filter applies a [[Kalman filter]] to a nonlinear model by linearizing at the current estimate. NASA developed it for Apollo navigation in the 1960s. Stanley F. Schmidt's work at Ames is the usual citation. The word "extended" means the linear algebra is wrapped around derivatives of a nonlinear function, not that the state got bigger.

## The problem

Attitude, GNSS, and a magnetometer are nonlinear functions of the state. A purely linear filter cannot represent a rotation. Linearizing is the cheapest way to keep the Kalman gain. It is a bad way when the linearization point is far from the truth, which is how an EKF diverges after a bad initial attitude.

## What you use it for

A practical drone state is: a small attitude error, velocity, position, gyro bias, accelerometer bias. Store the attitude as a [[Quaternion]]. Estimate the error, not the four quaternion entries. [[IMU mechanization]] is the predict step. GNSS and the barometer are the first updates. Add the magnetometer when yaw is the remaining hole.

[[EKF2]] is PX4's production version of this idea. Match its innovations before you match its code. If the linearization itself is the failure, the next filter is the [[Unscented Kalman filter]].

## See also

- [[Specific force]]
- [[Complementary filter]]
