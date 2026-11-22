---
type: concept
module: simulation
tags:
  - concept
  - simulation
status: article
aliases:
  - SDF worlds
  - SDFormat
---

# SDF

SDF, the Simulation Description Format, is the XML file [[Gazebo]] uses to describe a world and the objects in it. A file can place the ground, a building, a light, wind, and a robot, and it can set mass, inertia, and sensor poses. SDFormat is maintained as its own specification, split out from Gazebo's older XML so other tools can read it. The format grew up with Gazebo from the mid-2000s and became a separate library in the early 2010s.

## The problem

A scene that exists only as code is hard to share and hard to change without recompiling. A data file lets you move an obstacle or a spawn pose, and lets the simulator and the robot description stay in step.

## In this playground

`sim/worlds/quadcopter.sdf` is the aircraft, the ground, and the sensors. Another room or another wind is another file in that folder, passed to `gz sim`. Mass and motor constants live in the same file.

## See also

- [[Simulation]]
- [[Rigid-body quadrotor]]
