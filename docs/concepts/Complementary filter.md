---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Complementary filter

A complementary filter blends a fast sensor and a slow sensor that cover different frequency bands. Gyros are fast and they drift. Accelerometers and magnetometers are noisy and they do not drift in the same way. A high-pass on the gyro plus a low-pass on the accelerometer is a complementary filter for tilt. The idea is classical signal processing. The version drone firmware made standard is the nonlinear complementary filter on SO(3) by Mahony, Hamel, and Pflimlin, published in 2008.

## The problem

A full [[Extended Kalman filter]] is a lot of machinery if all you need is an attitude good enough to hover. The complementary filter is a few lines, with one gain that means "how much do I trust the accelerometer." It does not give you a careful [[Covariance]], and it is a weak position estimator.

## In this playground

Use it as the first attitude inside [[Control]], from specific force and the gyro. Replace it when you care about a full position state. There is no autopilot attitude to copy.

## See also

- [[Specific force]]
- [[Quaternion]]
