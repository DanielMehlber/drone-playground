---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
aliases:
  - inertial measurement unit
---

# IMU

An inertial measurement unit is a cluster of motion sensors fixed to the body. A modern board has three gyroscopes and three accelerometers, one pair along each axis. Gyros measure angular rate. Accelerometers measure [[Specific force]], which is acceleration including gravity, so a resting sensor reads about one g upward in the world, not zero.

## The problem

[[GNSS]] tells you where you are a few times a second, and it drops out indoors or near buildings. Between those fixes the aircraft still rotates and translates. The IMU is fast, typically hundreds to thousands of samples a second, so the [[Autopilot]] can integrate it. The cost is drift: small biases add up into a wrong attitude and a wrong position. That is why an estimator exists.

## Background

Aircraft used spinning-mass gyros through the twentieth century. Micro-electromechanical (MEMS) sensors reached cars in the 1990s. Chips such as the InvenSense MPU-6000, around 2010, made a full gyro-plus-accelerometer cheap enough for hobby quadrotors. A [[Pixhawk]] has one of these clusters on the board.

## In this playground

`/imu` is `sensor_msgs/Imu` in body forward-left-up. [[Control]] subscribes to it. Do not smooth it in the bridge. The noise is part of the problem. See [[Sensor noise]].

## See also

- [[EKF2]]
- [[Complementary filter]]
