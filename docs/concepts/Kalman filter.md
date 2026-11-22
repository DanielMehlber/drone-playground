---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
aliases:
  - KF
---

# Kalman filter

The Kalman filter is a [[Bayes filter]] for linear models and Gaussian noise. Rudolf E. Kálmán published it in 1960. Predict with a matrix F and a process-noise covariance Q. Update with a measurement matrix H, a measurement-noise covariance R, and a gain that balances the two. The gain is large when the measurement is trustworthy compared with the prediction.

## The problem

A linear blend of prediction and measurement needs a weight. Picking the weight by hand works for one sensor in one regime. The Kalman gain is that weight, computed so the resulting [[Covariance]] is as small as the noise model allows. It was built for navigation and tracking, where this loop runs forever.

## What you use it for

Build one on a line before you touch attitude: position and velocity, acceleration as the input, position as the measurement. Watch the [[Innovation]]. When that scalar filter is honest, the [[Extended Kalman filter]] is the same structure with F and H replaced by derivatives.

[[PX4 Autopilot|PX4]]'s [[EKF2]] is a much larger member of this family. It is the answer sheet, not the first exercise.

## See also

- [[Mahalanobis gate]]
- [[Sensor noise]]
