---
type: module
module: playground
tags:
  - module
---

# PX4 IO

Removed. The controller speaks ROS sensor messages and `actuator_msgs/Actuators` directly. Nothing in the running system converts PX4 frames, because PX4 is not running.

[[Coordinate frames]] in this setup are already ENU and body forward-left-up on both sides of the cable.

## See also

- [[Control]]
- [[PX4 Autopilot]]
