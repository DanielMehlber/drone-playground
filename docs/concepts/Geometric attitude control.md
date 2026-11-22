---
type: concept
module: control
tags:
  - concept
  - control
status: article
---

# Geometric attitude control

Geometric attitude control computes the rotation error on the rotation group itself, [[SO(3)]], or on its double cover, the unit [[Quaternion]]. Taeyoung Lee, Melvin Leok, and N. Harris McClamroch published the quadrotor version that labs still cite, "Geometric tracking control of a quadrotor UAV on SE(3)," in 2010. Thrust comes from the desired acceleration. Attitude error becomes a rate or a torque.

## The problem

[[Euler angles]] and a [[PID control|PID]] on them work near hover and fail when the chart fails. Aggressive flight and any path that passes near gimbal lock need an error that is a rotation, not three numbers with a seam.

## In this playground

Put it in [[Control]] as the attitude layer, and leave the rate layer as PID at first. That split is the one that transfers onto [[PX4 Autopilot|PX4]], which already accepts an attitude or a rate from [[Offboard mode]]. The quaternion must be body FLU in ENU. A mixed frame looks like the vehicle is upside down. See [[Quaternion]].

## See also

- [[Cascade control]]
- [[Coordinate frames]]
