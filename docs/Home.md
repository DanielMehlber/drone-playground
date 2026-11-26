---
type: module
module: playground
tags:
  - module
---

# Home

These notes are a small encyclopedia for this repo. Each page is one idea, one program, or one standard. It says what problem that thing solves, when it appeared, and where this playground uses it. Nothing here assumes you have built a drone before.

The graph colors module notes and concept notes as two groups. A link with no page is a topic the set does not cover yet. [[Adding a technique]] is how you add one. [[Concept index]] is the table of contents.

## If the words are new

Read in this order. Each page is short.

1. [[Quadrotor]]
2. [[Gazebo]] and [[SDF]]
3. [[IMU]], [[Barometer]], [[Magnetometer]], [[GNSS]]
4. [[ROS 2]]
5. [[Coordinate frames]]
6. [[Cascade control]] and [[PID control]]

Pages about [[PX4 Autopilot]], [[MAVLink]], and [[Micro XRCE-DDS]] stay in the vault as background. This repo does not run them.

## If you want to start building

The plant is [[Simulation]]. Your code is one program, [[Control]]. ROS 2 carries sensor samples one way and four rotor speeds the other way. The controller does not import Gazebo types, so a later hardware node can replace the bridge without rewriting the law.

Build the loops from the inside out. A route is a later publisher of setpoints. It is not part of this setup.

1. [[Simulation]]. Confirm the four sensors arrive and that no motor command is being sent.
2. [[Control]]. Rate, then attitude, then the height and position that hold a hover. The mixer that turns a desired force and torque into four speeds lives in the same package.
3. Check rotor order before the first non-zero command. Indices 0 and 1 turn one way, 2 and 3 the other. A swapped index flips the aircraft.
4. A filter, when you want one, is more code in the same package. It reads the same sensors. It does not need its own container.

## Containers

Open the repo root and reopen in the [[Dev containers|dev container]]: CUDA on Windows, Apple MPS on a Mac. Start each component in its own terminal. `compose.yaml` is for deployment: it starts the same components, one per container. [[Foxglove]] stays on Windows and is optional.
