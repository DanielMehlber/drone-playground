---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# Coordinate frames

A coordinate frame is a choice of origin and of three axis directions. The same physical point has different numbers in two frames. Drones inherit two choices that disagree, and most "the controller is unstable" afternoons are a disagreement about which one a number is in.

## The problem

[[PX4 Autopilot|PX4]] writes the world as NED: x north, y east, z down. It writes the body as FRD: x forward, y right, z down. That is the aviation convention, used in aircraft navigation for decades because altitude is naturally "down" in some older equations and north is a compass direction.

[[ROS 2]] writes the world as ENU: x east, y north, z up. It writes the body as FLU: x forward, y left, z up. That rule is [[REP-103]], from 2010. It matches robotics code, where z up is the usual picture of gravity.

## What you use it for

Gazebo and the controller both use ENU and body forward-left-up. There is no conversion node. North-east-down and body forward-right-down appear when you read [[PX4 Autopilot]] code. North in NED is +y in ENU. Right in FRD is −y in FLU. Down is −z in both maps.

Attitude is not a vector. Converting a [[Quaternion]] uses the same axis flip, a half turn about x, and the quaternion's own left-or-right convention. That page is separate because the sign error is worse.

## See also

- [[Euler angles]]
- [[Interfaces]]
