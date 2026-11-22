---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Bayes filter

A Bayes filter is the general shape of an estimator that repeats two steps. Predict: push the belief forward with a motion model. Update: correct it when a measurement arrives. The name comes from Thomas Bayes, whose essay on inverting probabilities was published in 1763. The recursive form used in tracking is twentieth-century work. Robotics took it up as a standard tool in the 1990s, and Probabilistic Robotics (Thrun, Burgard, and Fox, 2005) is the book that taught it to a generation of labs.

## The problem

Sensors disagree and arrive at different rates. You need a single belief about pose that can move between measurements and can change its mind when a measurement shows up. Ad hoc averaging has no place to put "I haven't seen GPS for a second."

## What you use it for

On this aircraft the predict step is [[IMU mechanization]]. The updates are [[GNSS]], the [[Barometer]], and the [[Magnetometer]]. The [[Kalman filter]] is the version where the belief is a Gaussian and the models are linear. The [[Extended Kalman filter]] is the one you will fly, because attitude is not linear.

Write predict and update as two functions from state to state. The ROS node only carries samples in and out.

## See also

- [[Covariance]]
- [[Estimation]]
