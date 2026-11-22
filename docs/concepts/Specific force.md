---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Specific force

Specific force is what an accelerometer measures: acceleration relative to free fall, not acceleration relative to the ground. A sensor sitting on the desk reads about 9.8 m/s² upward along the local vertical. In free fall it reads about zero. The name is standard in inertial navigation. The quantity has units of acceleration because mass has been divided out.

## The problem

If you integrate the accelerometer as if it were "acceleration in the world," you double-count gravity or you forget it, and the velocity ramps within seconds. [[IMU mechanization]] rotates the specific force into the world and then subtracts gravity. The rotation has to be right first, which is why attitude errors become position errors.

## In this playground

`/imu` calls the field `linear_acceleration` because that is the ROS habit, and the message comment says gravity is still in it. Treat the number as specific force when you write the predict step.

## See also

- [[IMU]]
- [[IMU mechanization]]
