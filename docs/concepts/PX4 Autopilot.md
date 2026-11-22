---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
aliases:
  - PX4
---

# PX4 Autopilot

PX4 is an open-source [[Autopilot]] for small aircraft, rovers, and boats. The flight code is C++. Modules inside one process talk on [[uORB]]. A [[Flight controller]] runs that process. A [[Companion computer]] can see the same topics through [[Micro XRCE-DDS]].

## The problem

Writing a motor mixer, a sensor driver, an estimator, and a failsafe, then keeping them matched to real boards, is a multi-year project. PX4 is the maintained version of that project, used so a control experiment can move onto hardware without inventing the rest of the aircraft.

## Background

The lineage is the PIXHAWK project at ETH Zurich, started around 2009 by Lorenz Meier and colleagues. The flight stack and the [[MAVLink]] protocol came out of that work in the following years. Since 2014 the project has lived under the Dronecode Foundation. Version 1.14, in 2023, made the new [[Gazebo]] the default simulator and replaced an older ROS 2 bridge with [[Micro XRCE-DDS]].

## In this playground

Not running. The inner loops are [[Control]], and the plant is [[Gazebo]] alone. PX4 remains the usual place those loops go when they move onto a [[Flight controller]]. Reading it is how you compare your mixer and your gains with a stack that already hovers.

## See also

- [[Pixhawk]]
- [[Offboard mode]]
- [[QGroundControl]]
