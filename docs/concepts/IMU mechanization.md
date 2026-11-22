---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# IMU mechanization

IMU mechanization is the set of equations that turn gyro and accelerometer samples into attitude, velocity, and position. Integrate angular rate to move the attitude. Rotate [[Specific force]] into the world, subtract gravity, and integrate for velocity and then position. Bias is a state you estimate, not a number you calibrate once.

The equations are the strapdown inertial navigation equations. "Strapdown" means the sensors are bolted to the body, and the old mechanical gimbal platform is replaced by software. That shift happened in aerospace in the 1960s, when computers could keep up with the gyros. Every [[Quadrotor]] estimator is a small strapdown navigator.

## The problem

Between [[GNSS]] fixes the aircraft still moves. Mechanization is how the belief keeps moving. A bias of a hundredth of a degree per second is invisible on a plot of the gyro and obvious as a drifting velocity a minute later.

## In this playground

This is the predict half of an [[Extended Kalman filter]] inside [[Control]], when you write one. Do it in body forward-left-up and world ENU. The samples on `/imu` are already in those frames. [[Sensor noise]] on the gyro is how fast the attitude [[Covariance]] is allowed to grow.

## See also

- [[IMU]]
- [[Coordinate frames]]
