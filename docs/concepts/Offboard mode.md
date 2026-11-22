---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# Offboard mode

Offboard mode is the [[PX4 Autopilot|PX4]] flight mode in which setpoints come from outside the autopilot, usually a [[Companion computer]]. A keepalive message, `OffboardControlMode`, must keep arriving. If it stops, PX4 leaves the mode and takes a failsafe action. The mode has been the supported way to fly from ROS for years. The message gained finer flags over time, including thrust-and-torque and direct motor commands.

## The problem

You want your own controller in the loop without deleting PX4's estimator, drivers, and [[Arming and failsafe]]. Offboard is that switch. A flag chooses which layer you replace. Direct actuator means motor commands, and PX4's position, attitude, and rate loops stay out of the way. Thrust-and-torque means you send a [[Wrench]] and PX4 still mixes. This playground's end state is direct actuator, with your own [[Allocation]].

## In this playground

Not used. The controller already owns the rotors. Offboard mode is the PX4 state in which an outside computer is allowed to send setpoints. You meet it if the inner loops later move into firmware and a companion only sends a position.

## See also

- [[Micro XRCE-DDS]]
- [[Cascade control]]
