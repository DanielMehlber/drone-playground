---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# EKF2

EKF2 is the name of the [[Extended Kalman filter]] built into [[PX4 Autopilot|PX4]]. The "2" is a generation count inside that project. It has been the default estimator since the late 2010s. It fuses the [[IMU]], [[GNSS]], [[Barometer]], [[Magnetometer]], and optional rangefinders, and it publishes the state the stock [[Cascade control|cascade]] flies on.

## The problem

Even if you intend to write your own filter, you need a working estimate on day one. Otherwise you cannot tell a bad gain from a bad predictor. EKF2 is that estimate, already tuned for the simulated sensors.

## In this playground

Not running. There is no autopilot estimate to copy. When you write a filter in [[Control]], EKF2 is the implementation to compare against, not a topic in this setup.

## See also

- [[Innovation]]
- [[Software in the loop]]
