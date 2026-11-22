---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
aliases:
  - Quaternion frames
---

# Quaternion

A quaternion is four numbers that represent a rotation. William Rowan Hamilton described them in 1843. Unit quaternions, those whose squares sum to 1, are the usual way to store attitude in an [[Autopilot]]. They do not suffer gimbal lock, the collapse [[Euler angles]] have when two axes line up.

## The problem

A rotation has three degrees of freedom, but any three-angle chart has a seam where the numbers jump or a degree of freedom disappears. Integrating a gyro in Euler angles stumbles on that seam. Integrating it in a quaternion does not. The cost is that the four numbers are less obvious to read, and multiplying them in the wrong order is a different rotation.

## In this playground

`sensor_msgs/Imu` carries orientation as a quaternion of the body in the world, [[REP-103]] style, when the simulator fills it. [[PX4 Autopilot]] stores body FRD in NED. The attitude map between those two is a 180 degree roll about the forward axis. You do not need that map while both sides of this setup are z-up. Check a known attitude before a controller uses the quaternion. Gazebo's IMU orientation is often the integrated gyro, not a heading fix. Prefer the gyro and the accelerometer for the first attitude loop.

[[Geometric attitude control]] consumes this quaternion. A mixed FRD/FLU quaternion looks like the aircraft is upside down.

## See also

- [[Euler angles]]
- [[IMU mechanization]]
