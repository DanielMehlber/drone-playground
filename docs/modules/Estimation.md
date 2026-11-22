---
type: module
module: playground
tags:
  - module
---

# Estimation

Not a separate program yet. When you write a filter, put it in the [[Control]] package and let the loops read its state in memory. The sensors are already on `/imu`, `/magnetometer`, `/air_pressure`, and `/navsat`.

Until that filter exists, the loops can use the IMU rates directly and a simple attitude from specific force and the magnetometer. Position hover can start from the GNSS and the barometer. A [[Kalman filter]] is the upgrade, not the first commit.

## See also

- [[IMU mechanization]]
- [[Extended Kalman filter]]
