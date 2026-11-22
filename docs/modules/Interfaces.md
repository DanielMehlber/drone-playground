---
type: module
module: playground
tags:
  - module
---

# Interfaces

There is no custom message package. The contract is the standard ROS types the bridge already converts:

- `sensor_msgs/Imu`, `MagneticField`, `FluidPressure`, `NavSatFix`
- `actuator_msgs/Actuators` for the four rotor speeds

A private message would have to be translated at the Gazebo boundary and again on a real aircraft. These types already have that translation.

## See also

- [[Control]]
- [[ROS 2]]
