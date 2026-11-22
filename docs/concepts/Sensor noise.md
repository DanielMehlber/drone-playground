---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Sensor noise

Sensor noise is the part of a reading that is not the quantity you wanted. For an [[IMU]], a usual model is white noise plus a bias that wanders like a slow random walk. For [[GNSS]], a usual first model is a jumpy position and velocity with a diagonal [[Covariance]] in ENU. Barometer noise is mostly height. Magnetometer noise is a direction, easily ruined by electrical current.

These models are engineering approximations from inertial navigation, written down in force during the strapdown era of the 1960s and 1970s, and reused on MEMS chips because the shape of the error is similar even though the physics of the chip is not.

## The problem

A filter that assumes perfect sensors will fit the noise and then drift. A filter that assumes ridiculous noise will ignore a good fix. The Q and R matrices are this model, written as numbers.

## In this playground

[[Simulation]] already applies a little noise on the IMU. The bridge passes it through. A filter inside [[Control]] is where it is modeled. If innovations are much smaller than your R, you told the filter the sensor was worse than it is.

## See also

- [[Kalman filter]]
- [[IMU mechanization]]
